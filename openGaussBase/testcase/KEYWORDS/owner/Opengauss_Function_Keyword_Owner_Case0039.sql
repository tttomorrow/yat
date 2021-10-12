--  @testpoint:opengauss关键字owner(非保留)，修改视图所有者

CREATE VIEW myView AS  SELECT * FROM pg_tablespace WHERE spcname = 'pg_default';

CREATE USER user_test1 IDENTIFIED BY 'Gs@123456';

ALTER VIEW  IF EXISTS  myView OWNER TO user_test1;

drop view myView;
drop user user_test1;
