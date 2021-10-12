--  @testpoint:openGauss关键字set(非保留),作为列名不带双引号，设置模式搜索路径。
 SET search_path TO tpcds, public;
--  @testpoint:openGauss关键字set(非保留), 把日期时间风格设置为传统的 POSTGRES 风格(日在月前)。 
 SET datestyle TO postgres;

