-- @testpoint: Hash分区表上以insert方式创建触发器

--step1：创建hash分区表、触发表 expect：成功
drop table if exists partition_hash_tab;
create table partition_hash_tab(p_id int)
partition by hash(p_id)
(partition p1,
 partition p2,
 partition p3,
 partition p4);
drop table if exists partition_hash_des_tab;
create table partition_hash_des_tab(p_id int);

--step2：创建触发器函数 expect：成功
CREATE OR REPLACE FUNCTION insert_func() RETURNS TRIGGER AS
           $$
           DECLARE
           BEGIN
                   INSERT INTO partition_hash_des_tab VALUES(1);
                   RETURN null;
           END
           $$ LANGUAGE PLPGSQL;
/

--step3：创建INSERT触发器 expect：成功
CREATE TRIGGER insert_trigger
           BEFORE INSERT ON partition_hash_tab
           FOR EACH ROW
           EXECUTE PROCEDURE insert_func();
/

--step4：插入数据 expect：成功
INSERT INTO partition_hash_tab VALUES(100);

--step5：查看触发器是否生效 expect：成功
SELECT * FROM partition_hash_des_tab;

--step6：清理环境 expect：成功
DROP TRIGGER insert_trigger on partition_hash_tab;
drop table if exists partition_hash_tab cascade;
drop table if exists partition_hash_des_tab cascade;
drop FUNCTION if exists insert_func();