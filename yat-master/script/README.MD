### ztools

ztools is the tool hub of zenith, and the main function of ztools is:

* install binary of zenith only
* create database data file and configure files and start a nomount instance
* create database data file and configure files and create a database
* kill instance
* kill instance and drop data and configure files


### zparam

zparam is the tool to read or write the zenith configure file

```bash
zparam write -i /path/to/zengine.in -w /path/to/new/zengine.ini -c LSNR_PORT=3001 -c _LOG_LEVEL=23
zparam read -i /path/to/zengine.ini -c LSNR_PORT
```

### zhba

zhba is the tool to read or write the zenith zhba.conf files

### imp_check/exp_check/load_check/dump_check

the zsql imp/exp/load/dump output filter which removing all the unused information

### ffi

file fault injection tools

