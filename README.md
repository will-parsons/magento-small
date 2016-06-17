Description
===========

#### Magento 2.x - Production

This stack is intended for low to medium traffic production websites and can be scaled as needed to accommodate future growth.
This stack includes a Cloud Load Balancer, Cloud Database, and a Primary web server (plus optional secondary servers).
It also includes Cloud Monitoring and Cloud Backups.

This stack is running:
- [NGINX](http://nginx.org/en/)
- [PHP FPM](http://php-fpm.org/about/)
- [Redis](http://redis.io/)
- Cloud Database running MySQL 5.6 where available
- The latest [Magento 2.x Community Edition](http://www.magentocommerce.com/product/community-edition/),
 - With the option, and full instructions, for uploading an existing Magento site.


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
provided in the "Credentials" section of Stack Details.

#### Logging in via SSH
To update or upload code, you can log in as the 'magento' user via SSH or SFTP
into the 'httpdocs' folder. The password is provided n the "Credentials"
section of Stack Details.

The private key provided in the passwords section can be used to login as
root via SSH, which should be used for configuration changes only.
We have an article on how to use these keys with [Mac OS X and
Linux](http://www.rackspace.com/knowledge_center/article/logging-in-with-a-ssh-private-key-on-linuxmac)
as well as [Windows using
PuTTY](http://www.rackspace.com/knowledge_center/article/logging-in-with-a-ssh-private-key-on-windows).

#### Details of Your Setup
This deployment was stood up using [Ansible](http://www.ansible.com/).  Once
the deployment is up, Ansible will not run again unless you update the
stack. **Any changes made to the configuration may be overwritten when the
stack is updated.**

[Varnish](https://www.varnish-cache.org) is in use for Magento Full Page Cache. 
VCL configuration is from [Magento2 source](https://github.com/magento/magento2/blob/2.0/app/code/Magento/PageCache/etc/varnish4.vcl)


[Nginx](http://nginx.org/en/) is used as the web server and listens on port
8080 to handle web traffic. Configuration follows [Magento2 source](https://github.com/magento/magento2/blob/2.0/nginx.conf.sample) and can be found in /etc/nginx/conf.d/. There will be a default site
configuration and a separate one for your domain. Magento itself is
installed in /var/www/vhosts. You will find a directory with the name of
website you entered as a part of this deployment.

[PHP-FPM](http://php.net/manual/en/install.fpm.php) is used to handle
evaluation of all PHP-based pages. The configuration for this installation is
based on the URL of your site, and can be found within
/etc/php5/fpm/pools/yoursite.conf.  Nginx is configured to send Magento Admin
Dashboard trafic to a second PHP-FPM pool for better memory management.

Magento cache backend is stored in [Redis](http://redis.io/). 
Redis is an in-memory, high performance key-value
and is used for caching data and persisting user session data. This enhances
the performance of your site by reducing expensive database calls. Three
caches are configured: two for data caching and one for session persistence.
You can find the configuration of these caches in /etc/redis/.

Redis is running on the Primary server, and relevant Magento
configuration is under: app/etc/env.php
If you plan to replace the default Magento codebase with your own store, you
should take a copy of these files for reference. 

For a more resiliend cache backend, ask your support team about setting up
a hosted Redis instance on our ObjectRocket platform. 


MySQL is being hosted on a Cloud Database instance.
Backups for MySQL are provided by [Holland](http://wiki.hollandbackup.org/),
which is running on the Primary web server.

Backups are configured using Cloud Backups.  The Primary server is configured
to back up /var/spool/holland and /var/www once per week, and to retain
these backups for 30 days.

In order to restore the Database from backup, you will need to first restore
/var/spool/holland from the appropriate Cloud Backup.  After you have done so,
you will need to log into the Primary server and restore the Holland backup
to the Cloud Database via the MySQL client.  For more assistance, please
contact your Support team.

Monitoring is configured to verify that Nginx is running on both the Primary
and all secondary servers, as well as that the Cloud Load Balancer is
functioning.  Additionally, the default CPU, RAM, and Filesystem checks
are in place on all servers.

### Notes for multi-server deployments
On the secondary servers, Nginx is configured to sent all Magento Admin
Dashboard traffic to the Primary web server; (proxy_pass if adminhtml cookie
is present.) This avoids the need to use a separate DNS subdomain for your
Admin traffic, and ensures all new content, such as product images, are
uploaded to the Primary server.

[Lsyncd](https://github.com/axkibe/lsyncd) has been installed in order to
sync static content from the Primary server to all secondary servers.
When uploading content, it only needs to be uploaded to the Primary node,
and will be automatically synchronized to all secondary nodes.

### SSL Certificates
Using SSL is highly recommended. You can enable SSL by uploading your
certificate to the Cloud Load Balancer, which is configurable under Network ->
Cloud Load Balancers. Once it is set up, you can set your Frontend and Admin
use https:// base URLs. Please call Support for further guidance, or if your
actions lead to broken or looping redirects.

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

#### Important security notes
The Magento code provided here is the latest at time of deployment, but
Magento does *not* auto-update. You, or your development team, are responsible
for applying any and all future Magento security patches to keep your site
secure. For awareness, we would highly recommend signing up to recieve
security alerts at https://magento.com/security

#### Uploading your existing Magento Website
If you already have an existing Magento website to import to this solution,
you should select the "Do not install Magento" option under Advanced Options,
and follow these steps.

#####1. Code upload

Use the `magento` SSH credentials to upload your code and content, via SFTP,
into to the `~/httpdocs` directory on the primary web server. The *LsyncD*
will synchronise content to any secondary servers.

#####2. Database import

Upload your database dump to the master server with the `magento` SSH
credentials. Put in in the home directory, above httpdocs, so that it's not
accessible over the web. We've set up credentials in the `~/.my.cnf` for you
to easily use the mysql command line client. The database will be called
`magento`.

Log on via SSH as the 'magento' user, and import with:

```mysql magento < your-database-dump.sql```
or, if it's compressed:
```zcat your-database-dump.sql.gz | mysql magento```

This can typically take up to 20 minutes, depending on your database size.

> Alternatively, you could use the MySQL Workbench or similar, using
> "TCP/IP over SSH". First use the `magento` SSH credentials for the SSH
> tunnel, then the Cloud Database hostname and MySQL credentials.


#####3. Magento Database configuration

Modify your `app/etc/env.php` file with the Cloud Database details. The
database name is `magento`and the database username is `magento`. The hostname
will be your unique `xxxxx.rackspaceclouddb.com` host, and the password can be
found in the Stack Credentials and also in your `~/.my.cnf` file on the
primary web server.

#####4. Magento cache configuration

This step is *essential* for performance, and for the correct operation of
multi-server setups.

You should find the necessary config under `~/httpdocs/app/etc/env.php`,
which will be included by Magento if kept in that directory. If this has been
overwritten or removed by your version control or, you should also find the
details in `~/env.php.example`, which you can include in your own `env.php`.

There are multiple Redis instances running on the primary web server for
Magento sessions and Magento cache backend. Note that in order to use Redis
for sessions, you will also need to modify
`app/etc/modules/Cm_RedisSession.xml` and set `<active>` to "true" . The
fallback is to use the database.

Please do contact Rackspace support if you need assistance here, or if you'd
like to discuss using the highly available ObjectRocket platform for Redis.

#####4. Magento sessions configuration

- In Magento 2.0, Redis support for sessions was dropped. 
- Memcached for PHP 7.0 is [not stable yet](https://github.com/iuscommunity/wishlist/issues/38)
- Recommend using files for the time being, or Database for multi-server architectures.
- Subject to change when php70u-memcached is available or if Magento reintroduce the Cm_RedisSession module for Magento2. 


#####6. Final steps

- You may wish to disable Magento's automatic redirection, in order to access
the Admin dashboard for testing and URL configuration.

> Log on via SSH as the 'magento' user, then you can set that with:
>
>     mysql magento -e 'UPDATE core_config_data SET value=0 WHERE path="web/url/redirect_to_base"';

- Delete all files under `httpdocs/var/cache` left over from any
   previous environments.

- If we can help at any stage, please don't hesitate to call
   Rackspace Support and our Magento experts will be happy to advise on
   all aspects of your deployment.


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
* `magento_install`: This option determines whether or not to install Magento and/or the sample
data, or if you will need to upload your own Magento code.
 (Default: Fresh install of the latest Magento CE 1.9.x release)
* `server_flavor`: Flavor of Cloud Server to use for Magento (Default: 8 GB General Purpose v1)
* `server_image`: (Default: f4bbbce2-50b0-4b07-bf09-96c175a45f4b)
* `database_disk`: Size of the Magento Cloud Database volume in GB (Default: 10)
* `database_flavor`: Flavor for the Magento Cloud Database (Default: 4GB Instance)
* `server_count`: Number of secondary servers to create.  These will be synchronized from the primary node (Default: 0)
* `secondary_template`: Template to use for secondary servers (Default: https://raw.githubusercontent.com/rackspace-orchestration-templates/magento-small/stable/magento_small_secondary.yaml)
* `ansible_branch`: The Ansible Roles will be pulled from Git, using the tag or branch provided (Default: stable)
* `ansible_repo`: The Ansible Roles will be pulled from Git, using the repo provided (Default: https://github.com/rackspace-orchestration-templates/ansible-roles.git)

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
* `server_ip`: Primary Server Public IP 
* `ssh_password`: Magento SSH Password 
* `secondary_ips`: Secondary Node IPs 

For multi-line values, the response will come in an escaped form. To get rid of
the escapes, use `echo -e '<STRING>' > file.txt`. For vim users, a substitution
can be done within a file using `%s/\\n/\r/g`.
