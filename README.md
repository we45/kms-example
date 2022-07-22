### AWS KMS Example

* Step 1: Create AWS account and initialize
    * Once you provision the server Click on `Access` button. 
    * In the appeared window click on `Terminal` and select `New terminal`

```bash
asectl init aws
```

* Step 2: Change to directory
```bash
cd /root/kms-example
```

* Step 3: Create a CMK key and export it as environment variable. 
```bash
export cmk_id=$(aws kms create-key  --tags TagKey=ASE,TagValue=KMS --description "Serverless secure coding" --query KeyMetadata.KeyId --output text)
```

* Step 3: Let's run the KMS example
```bash
python3 app.py
```

### Teardown

* Step 1:  press `ctrl + c` to stop the KMS example application 

``` bash
exit
```
* Step 2: Let's delete the KMS key with scheduled deletion set to `7 days`


```bash
aws kms schedule-key-deletion  --key-id $cmk_id  --pending-window-in-days 7
```