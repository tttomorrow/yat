-- @testpoint: 设置客户端编码格式后查询
set client_encoding to 'utf8';
SELECT pg_client_encoding();
set client_encoding to 'utf8';