-- @describe: 存储过程中调试语句  info


CREATE OR REPLACE PROCEDURE proc_raise3(user_id in integer)
AS
BEGIN
RAISE info  'Noexistence ID --> %',user_id USING HINT = 'Please check your user ID';
END;
/

call proc_raise3(300011);
drop PROCEDURE proc_raise3;