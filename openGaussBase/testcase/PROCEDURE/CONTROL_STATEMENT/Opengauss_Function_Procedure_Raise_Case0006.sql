-- @describe: 存储过程中调试语句


CREATE OR REPLACE PROCEDURE proc_raise6(user_id in integer)
AS
BEGIN
RAISE EXCEPTION  'Noexistence ID --> %',user_id USING HINT = 'Please check your user ID';
END;
/

call proc_raise6(300011);
drop PROCEDURE proc_raise6;