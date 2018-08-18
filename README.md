#### Prerequisites
* python 2.7.14 installed
* SSH keys providing access to the environment provisioned
* Terraform
* Templates which setup [basic two-tier AWS architecture](https://github.com/terraform-providers/terraform-provider-aws/tree/master/examples/two-tier)
* SSH config file

##### SSH config file
```
$ cat ~/.ssh/config
Host <public_ip>
    User ubuntu
    IdentitiesOnly yes
    IdentityFile ~/.ssh/<your_key>
```

clone repository

* `cd infra_test`
* `pip install -r requirements.txt`
* `export PUBLIC_DNS=<public_dns if it is presented in terraform show output else empty>`
* `export PUBLIC_IP=<public_ip if it is presented in terraform show output else empty>`
* `export SSH_CONFIG_DIR=<path to dir containing your ssh config file>`
* `./run_tests.sh`
