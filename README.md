Description
===========

#### Production

This stack is intended for low to medium traffic production
websites and can be scaled as needed to accommodate future
growth.  This stack includes a Cloud Load Balancer, Cloud
Database, and a Master server (plus optional secondary
servers).  It also includes Cloud Monitoring and Cloud
Backups.

This stack is running
[Magento 1.9.2.0 Community Edition](http://www.magentocommerce.com/product/community-edition/),
[nginx](http://nginx.org/en/),
and [PHP FPM](http://php-fpm.org/about/).
with a Cloud Database running
[Percona](https://www.percona.com/software/mysql-database/percona-server).


Instructions
===========

#### Getting Started
If you're new to Magento Community Edition, the [Magento User
Guide](http://www.magentocommerce.com/resources/user-guide-download) will
step you through the process of configuring and managing your store. This
guide is free, but does require you to provide a valid email address to
receive it.

After the stack has been created, you can find the admin username and
password listed in the "Credentials" section of Stack Details.

The [Magento Forum](http://www.magentocommerce.com/boards/) provides a place
to get answers to both simple and advanced questions regarding configuration
and management of Magento Community Edition.

#### Logging into Magento
To login, go to the URL listed above in a browser. If your DNS is not
pointing to this installation, you can add a line in your [hosts
file](http://www.rackspace.com/knowledge_center/article/how-do-i-modify-my-hosts-file)
to point your domain to the IP of this Cloud Server. Once you've done this,
restart your browser and navigate to the site. The backend can be accessed using the
"Magento Admin URL" listed in Stack Details, and you can login with the credentials
provided in the "Credentials" section of Stack Details..

#### Logging in via SSH
The private key provided in the passwords section can be used to login as
root via SSH. We have an article on how to use these keys with [Mac OS X and
Linux](http://www.rackspace.com/knowledge_center/article/logging-in-with-a-ssh-private-key-on-linuxmac)
as well as [Windows using
PuTTY](http://www.rackspace.com/knowledge_center/article/logging-in-with-a-ssh-private-key-on-windows).

#### Details of Your Setup
This deployment was stood up using [Ansible](http://www.ansible.com/).  Once
the deployment is up, Ansible will not run again unless you update the
stack. **Any changes made to the configuration may be overwritten when the stack
is updated.**

[Nginx](http://nginx.org/en/) is used as the web server and listens on port
80 to handle web traffic. The configuration for your site can be
found in /etc/nginx/conf.d/. There will be a default site
configuration and a separate one for your domain. Magento itself is
installed in /var/www/vhosts. You will find a directory with the name of
website you entered as a part of this deployment.

[PHP-FPM](http://php.net/manual/en/install.fpm.php) is used to handle
evaluation of all PHP-based pages. The configuration for this installation is
based on the URL of your site, and can be found within  /etc/php5/fpm/pools/yoursite.conf.
By default, PHP-FPM is running as the 'magento' user, listens on 127.0.0.1:9001.

Object and session caching are handled by
[Redis](http://redis.io/). Redis is an in-memory, high performance key-value
and is used for caching data and persisting user session data. This enhances
the performance of your site by reducing expensive database calls. Three caches
are configured: two for data caching and one for session persistence. You can
find the configuration of these caches in /etc/redis/.

[Lsyncd](https://github.com/axkibe/lsyncd) has been installed in order to
sync static content from the Master server to all secondary servers.
When uploading content, it only needs to be uploaded to the Master node,
and will be automatically synchronized to all secondary nodes.

MySQL is being hosted on a Cloud Database instance, running MySQL 5.6.
Backups for MySQL are provided by [Holland](http://wiki.hollandbackup.org/),
which is running on the Master server.

Backups are configured using Cloud Backups.  The Master server is configured
to back up /var/spool/holland and /var/www once per week, and to retain
these backups for 30 days.

In order to restore the Database from backup, you will need to first restore
/var/spool/holland from the appropriate Cloud Backup.  After you have done so,
you will need to log into the Master server and restore the Holland backup
to the Cloud Database via the MySQL client.  For more assistance, please
contact your Support team.

Monitoring is configured to verify that Apache is running on both the Master
and all secondary servers, as well as that the Cloud Load Balancer is
functioning.  Additionally, the default CPU, RAM, and Filesystem checks
are in place on all servers.

#### Magento Plugins
There are thousands of plugins that have been developed for Magento by the
developer community. [Magento
Connect](http://www.magentocommerce.com/magento-connect/) provides an easy
way to discover popular plugins that other users have found to be helpful.
Not all plugins are free, and we recommend only installing the plugins that
you need.

#### Additional Notes
You can add additional servers to this deployment by updating the
"server_count" parameter for this stack.  This deployment is
intended for low to medium traffic production websites and can be
scaled as needed to accommodate future growth.

When scaling this deployment by adjusting the "server_count" parameter,
make sure that you DO NOT change the "database_flavor" and "database_disk"
parameters, as this will result in the loss of all data within the
database.

This stack will not ensure that Magento or the servers themselves are
up-to-date.  You are responsible for ensuring that all software is
updated.


Requirements
============
* A Heat provider that supports the following:
  * OS::Heat::RandomString
  * OS::Heat::ResourceGroup
  * OS::Heat::SoftwareConfig
  * OS::Heat::SoftwareDeployment
  * OS::Nova::KeyPair
  * OS::Nova::Server
  * OS::Trove::Instance
  * Rackspace::Cloud::BackupConfig
  * Rackspace::Cloud::LoadBalancer
  * Rackspace::CloudMonitoring::Check
* An OpenStack username, password, and tenant id.
* [python-heatclient](https://github.com/openstack/python-heatclient)
`>= v0.2.8`:

```bash
pip install python-heatclient
```

We recommend installing the client within a [Python virtual
environment](http://www.virtualenv.org/).

Parameters
==========
Parameters can be replaced with your own values when standing up a stack. Use
the `-P` flag to specify a custom parameter.

* `magento_url`: Domain to use with Magento Site (Default: example.com)
* `magento_user`: Username for Magento admin (Default: admin)
* `magento_fname`: First name for Magento admin (Default: Joe)
* `magento_lname`: Last name for Magento admin (Default: User)
* `magento_email`: E-Mail for Magento admin (Default: admin@example.com)
* `magento_eula`: You must agree to the terms of the Magento Community Edition License 
* `magento_samples`: Include Magento Sample Data (Default: False)
* `server_flavor`: Flavor of Cloud Server to use for Magento (Default: 8 GB General Purpose v1)
* `database_disk`: Size of the Magento Cloud Database volume in GB (Default: 10)
* `database_flavor`: Flavor for the Magento Cloud Database (Default: 4GB Instance)
* `server_count`: Number of secondary servers to create.  These will be synchronized from the primary node (Default: 0)

Outputs
=======
Once a stack comes online, use `heat output-list` to see all available outputs.
Use `heat output-show <OUTPUT NAME>` to get the value of a specific output.

* `magento_login_user`: Magento Admin User 
* `magento_login_password`: Magento Admin Password 
* `magento_public_ip`: Load Balancer IP 
* `magento_admin_url`: Magento Admin URL 
* `magento_public_url`: Magento Public URL 
* `mysql_user`: Database User 
* `mysql_password`: Database Password 
* `ssh_private_key`: SSH Private Key 
* `server_ip`: Server Public IP 
* `secondary_ips`: Secondary Node IPs 

For multi-line values, the response will come in an escaped form. To get rid of
the escapes, use `echo -e '<STRING>' > file.txt`. For vim users, a substitution
can be done within a file using `%s/\\n/\r/g`.
