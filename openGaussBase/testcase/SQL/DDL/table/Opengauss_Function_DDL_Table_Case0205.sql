-- @testpoint: alter table constraint_clause PARTITION
--正常
DROP TABLE IF EXISTS al_table_9;
CREATE TABLE al_table_9(c1 int, c2 varchar(32), c3 bigint) PARTITION BY RANGE(c1) (PARTITION p1 VALUES LESS THAN (100), PARTITION p2 VALUES LESS THAN (200), PARTITION p3 VALUES LESS THAN (300), PARTITION p4 VALUES LESS THAN (maxvalue));
INSERT INTO al_table_9 VALUES(50, 'P1', 5000);
INSERT INTO al_table_9 VALUES(150, 'P2', 15000);
INSERT INTO al_table_9 VALUES(250, 'P3', 25000);
INSERT INTO al_table_9 VALUES(350, 'P4', 35000);
COMMIT;
alter table al_table_9 drop PARTITION p1;
alter table al_table_9 truncate PARTITION p2;
--defult ''
DROP TABLE IF EXISTS al_table_9;
CREATE TABLE al_table_9(c1 int default '', c2 varchar(32) default '', c3 bigint default '') PARTITION BY RANGE(c1) (PARTITION p1 VALUES LESS THAN (100), PARTITION p2 VALUES LESS THAN (200), PARTITION p3 VALUES LESS THAN (300), PARTITION p4 VALUES LESS THAN (maxvalue));
INSERT INTO al_table_9 VALUES(50, 'P1', 5000);
INSERT INTO al_table_9 VALUES(150, 'P2', 15000);
INSERT INTO al_table_9 VALUES(250, 'P3', 25000);
INSERT INTO al_table_9 VALUES(350, 'P4', 35000);
COMMIT;
alter table al_table_9 drop PARTITION p1;
alter table al_table_9 truncate PARTITION p2;
DROP TABLE IF EXISTS al_table_9;
