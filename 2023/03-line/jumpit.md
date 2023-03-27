# jumpit

- Japanese ver: <https://project-euphoria.dev/blog/40-line-ctf-2023/#jumpit>

We are given an unzipped APK including native libraries. One of them is `libil2cpp.so` that is created by "il2cpp". After googling about il2cpp, I found [Perfare/Il2CppDumper: Unity il2cpp reverse engineer](https://github.com/Perfare/Il2CppDumper). Using this tool, I got restored dlls, header file, a JSON that has stringLiteral informations, etc.

I analyzed the dll using dnSpy and found some functions about the application. One of them is `GameManager$$GetFlag` and the decompiled code is here.

```c
void GameManager$$GetFlag(long param_1,undefined8 param_2,int param_3)

{
  ulong uVar1;
  undefined8 uVar2;
  long *plVar3;
  
  if ((DAT_00c141f3 & 1) == 0) {
    thunk_FUN_0037eb0c(&StringLiteral_3273);
    thunk_FUN_0037eb0c(&StringLiteral_2608);
    DAT_00c141f3 = 1;
  }
  if ((param_3 == 0x1077) &&
     (uVar1 = System.String$$op_Equality(param_2,StringLiteral_3273,0), (uVar1 & 1) != 0)) {
    uVar2 = GameManager$$DecryptECB(uVar1,*(undefined8 *)(param_1 + 0x50),StringLiteral_2608);
    plVar3 = *(long **)(param_1 + 0x30);
    if (plVar3 != (long *)0x0) {
                    /* WARNING: Could not recover jumptable at 0x008b7e34. Too many branches */
                    /* WARNING: Treating indirect jump as call */
      (**(code **)(*plVar3 + 0x558))(plVar3,uVar2,*(undefined8 *)(*plVar3 + 0x560));
      return;
    }
                    /* WARNING: Subroutine does not return */
    FUN_003d9d08();
  }
  return;
}
```

I guessed that `uVar2` is the flag and this value is decrypted by AES-ECB. Accrding to the header file gotten from Il2CppDumper, the function signature of `GameManager$$DecryptECB` is `public string DecryptECB(string keyString, string text) { }`. So, the key is `param_1 + 0x50` and the cipher text is `StringLiteral_2608`.

I also guessed `param_1` is the instance of `GameManager`. From the header file, the fields and methods of `GameManager` are here.

```c#
public class GameManager : MonoBehaviour // TypeDefIndex: 2677
{
	// Fields
	private int scoreTarget; // 0x18
	private int score; // 0x1C
	public GameObject obstacle; // 0x20
	public Transform spawnPoint; // 0x28
	public TextMeshProUGUI scoreText; // 0x30
	public GameObject playButton; // 0x38
	public GameObject player; // 0x40
	public string rootDetectedMsg; // 0x48
	private string finalKey; // 0x50

	// Methods

	// RVA: 0x7B7908 Offset: 0x7B7908 VA: 0x7B7908
	private void Start() { }

	// RVA: 0x7B7A20 Offset: 0x7B7A20 VA: 0x7B7A20
	private void Update() { }

	[IteratorStateMachineAttribute] // RVA: 0x2520F0 Offset: 0x2520F0 VA: 0x2520F0
	// RVA: 0x7B7A24 Offset: 0x7B7A24 VA: 0x7B7A24
	private IEnumerator SpawnObstacles() { }

	// RVA: 0x7B7AC8 Offset: 0x7B7AC8 VA: 0x7B7AC8
	private void ScoreUp() { }

	// RVA: 0x7B7D88 Offset: 0x7B7D88 VA: 0x7B7D88
	public void GetFlag(string text, int score) { }

	// RVA: 0x7B81A0 Offset: 0x7B81A0 VA: 0x7B81A0
	public void GameStart() { }

	// RVA: 0x7B82B0 Offset: 0x7B82B0 VA: 0x7B82B0
	public string EncryptECB(string keyString, string text) { }

	// RVA: 0x7B7E4C Offset: 0x7B7E4C VA: 0x7B7E4C
	public string DecryptECB(string keyString, string text) { }

	// RVA: 0x7B79A4 Offset: 0x7B79A4 VA: 0x7B79A4
	private bool IsDeviceRooted() { }

	// RVA: 0x7B85F8 Offset: 0x7B85F8 VA: 0x7B85F8
	public void .ctor() { }
}
```

`param_1 + 0x50` is `finalKey`. I searched methods that assign some values to this field and found `ScoreUp`. The part of decompiled code is here.

```c
  if (iVar2 < 500000) {
    if (iVar2 < 3000) {
      if (iVar2 == 10) {
        uVar1 = *(undefined8 *)(param_1 + 0x50);
        puVar3 = &StringLiteral_679;
        goto LAB_008b7ce8;
      }
      if (iVar2 == 200) {
        uVar1 = *(undefined8 *)(param_1 + 0x50);
        puVar3 = &StringLiteral_107;
        goto LAB_008b7ce8;
      }
    }
    else {
      if (iVar2 == 3000) {
        uVar1 = *(undefined8 *)(param_1 + 0x50);
        puVar3 = &StringLiteral_297;
        goto LAB_008b7ce8;
      }
      if (iVar2 == 40000) {
        uVar1 = *(undefined8 *)(param_1 + 0x50);
        puVar3 = &StringLiteral_2389;
        goto LAB_008b7ce8;
      }
    }
  }
```

When the score (`iVar2`) reaches certain values, a string (`StringLiteral_...`) is concatenated with the key (`param_1 + 0x50`) in `LAB_008b7ce8`. We can recover the full part of key because all `StringLiteral...` are known from the JSON (`stringliteral.json`) that is given by the dumper.

Now, we have the key and the cipher text. So we can get the flag by just decrypting it. I used this code.

```python
from Crypto.Cipher import AES

# from `System.Convert$$FromBase64String(StringLiteral_2608)`
ct = "71-61-93-99-E0-E5-16-C6-04-14-8F-44-E6-61-FF-78-29-D0-D5-23-65-58-99-57-8F-E9-25-3C-B6-D6-4B-F7-3F-D6-F2-3B-50-FA-CE-E1-DA-78-D6-ED-AD-4C-63-36"
ct = list(map(lambda x: int(x,16), ct.split("-")))

print(ct)
print(len(ct))

key = "Cia!fo2MPXZQvaVA39iuiokE6cvZUkqx"
print(len(key))

cipher = AES.new(key.encode(), AES.MODE_ECB)
pt = cipher.decrypt(bytes(ct))

print(pt)
```

- flag: `LINECTF{1c4f5397798d9150ce1b8e10e9d99657}`
