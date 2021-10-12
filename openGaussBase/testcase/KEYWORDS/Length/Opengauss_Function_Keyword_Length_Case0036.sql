--  @testpoint:opengauss关键字Length(非保留)，指定encoding编码格式的string的字符数。在这个编码格式中，string必须是有效的
SELECT length('jose', 'UTF8');
SELECT length('jose', 'GBK');
SELECT length('jose', 'SQL_ASCII');
SELECT length('jose', 'LATIN1');