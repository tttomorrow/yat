-- @testpoint: 初始化BLOB值
drop table if exists blob_tb;
CREATE TABLE blob_tb(b blob,id int);
INSERT INTO blob_tb VALUES (empty_blob(),1);
select * from blob_tb;
DROP TABLE blob_tb;