-- @testpoint: 列存表的表级PARTIAL CLUSTER KEY约束。


DROP TABLE IF EXISTS tab_12;
CREATE TABLE tab_12
(id                     NUMBER(7),
 use_filename              VARCHAR2(20),
 filename                  VARCHAR2(255),
 text                       VARCHAR2(2000),
 PARTIAL CLUSTER KEY (id))
 with(ORIENTATION=COLUMN);

insert into tab_12 values(1,'李','小龙','截拳道大师');
insert into tab_12 values(2,'zhang','小gou','空手道道大师');
insert into tab_12 values(3,'wan123','xiaoxiao','跆拳道大师');
select * from  tab_12;
drop table if exists tab_12;

