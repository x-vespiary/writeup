# Lootout Foxy

## Writeup

To tell the truth, I couldn't solve this challenge because of my trivial mistake...  
This writeup shows the solution I tried after CTF.

In this challenge, we were given disk dump and I used autopsy. I  noticed that autopsy was so useful tool!!

### Outlook Express analysis

First, I analysed the data about email. In this system, Outlook Express is installed. So I googled `outlook express data file location` and knew that mail data is stored at `/Documents and Settings/<user name>/Local Settings/Application Data/Identities/<{long id}>/Microsoft/Outlook Express`.

In this directory, some files whose extension is `.dbx`. Some tools converts a `.dbx` file to a populer extension file (Sorry, I forgot the tools I used...).

I found the embedded file named `secret.gpg`. This is encrypted file by gpg key.

```
$ file secret.gpg 
secret.gpg: PGP RSA encrypted session key - keyid: F22AEE21 2BEB18B8 RSA (Encrypt or Sign) 3072b .
```

I misunderstood about this file. I regarded this file as a "gpg key as binary". As a result, even though I was able to find gpg key, I couldn't solve this challenge and this was my worst CTF mistake in 2020 lol.

Anyway, I got encrypted data, so I searched the key and found it (located at `/Program Files/GPG/secret.key`). These commands were executed at the decryption.

```
$ gpg --import secret.key
...
$ gpg -o out -d secret.gpg
$ cat out | grep inctf
Important string: inctf{!_h0p3_y0u_L1k3d_s0lv1ng_7h3_F1rs7_p4r7_ 
```

I got the half of flag!!

### Firefox analysis

Second, I analysed web data such as browser history and search history. Autopsy gathered these information (this was so useful!!).

In search history, user (whose name is crimson) searched `can we decrypt saved passwords`. I googled same words and read the websites showed in results.

According to this [website](https://null-byte.wonderhowto.com/how-to/hacking-windows-10-steal-decrypt-passwords-stored-chrome-firefox-remotely-0183600/), we can extract login credentials from firefox data by [this tool](https://github.com/Unode/firefox_decrypt). So I cloned it and extract credentials.

```
$ python firefox_decrypt.py /mnt/e/autopsy_base/foxy/Export/524-Profiles/5ztdm4br.default/
2020-08-04 11:43:57,819 - WARNING - profile.ini not found in /mnt/e/autopsy_base/foxy/Export/524-Profiles/5ztdm4br.default/
2020-08-04 11:43:57,819 - WARNING - Continuing and assuming '/mnt/e/autopsy_base/foxy/Export/524-Profiles/5ztdm4br.default/' is a profile location

Master Password for profile /mnt/e/autopsy_base/foxy/Export/524-Profiles/5ztdm4br.default/: 
2020-08-04 11:43:58,743 - WARNING - Attempting decryption with no Master Password

Website:   http://35.209.205.103
Username: 'Danial_Banjamin'
Password: '2!6BQ&e626g#YNWxsQWV9^knO8#85*E%6Zaxr@At42'
```

I got the credential of `http://35.209.205.103`. I accessed and attempt to login. After login, second part of the flag was displayed!!

## Flag

`inctf{!_h0p3_y0u_L1k3d_s0lv1ng_7h3_F1rs7_p4r7_4nd_3njoy3d_7he_53c0nd_p4rt_0f_7h3_ch4ll3ng3}`

## References

1. <https://null-byte.wonderhowto.com/how-to/hacking-windows-10-steal-decrypt-passwords-stored-chrome-firefox-remotely-0183600/>
2. <https://github.com/Unode/firefox_decrypt>
