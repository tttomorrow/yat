--  @testpoint: --创建序列名称验证大小写
drop TABLE IF EXISTS customer_address CASCADE;
 CREATE TABLE customer_address
(
    ca_address_sk             integer               not null,
    ca_address_id             char(16)              not null,
    ca_street_number          char(10)                      ,
    ca_street_name            varchar(60)                   ,
    ca_street_type            char(15)                      ,
    ca_suite_number           char(10)                      ,
    ca_city                   varchar(60)                   ,
    ca_county                 varchar(30)                   ,
    ca_state                  char(2)                       ,
    ca_zip                    char(10)                      ,
    ca_country                varchar(20)                   ,
    ca_gmt_offset             decimal(5,2)                  ,
    ca_location_type          char(20)
);
--创建序列
drop SEQUENCE IF EXISTS ss CASCADE;
CREATE SEQUENCE ss OWNED BY customer_address.ca_address_sk;
CREATE SEQUENCE SS OWNED BY customer_address.ca_street_number;
CREATE SEQUENCE "SS" OWNED BY customer_address.ca_street_number;
--清理
drop SEQUENCE IF EXISTS ss CASCADE;
drop SEQUENCE IF EXISTS SS CASCADE;
drop TABLE IF EXISTS customer_address CASCADE;