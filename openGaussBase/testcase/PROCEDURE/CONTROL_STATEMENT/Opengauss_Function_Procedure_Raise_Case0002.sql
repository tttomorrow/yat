-- @describe: 存储过程中调试语句 log


CREATE OR REPLACE PROCEDURE proc_raise2(user_id in integer)
AS
BEGIN
RAISE log 'Noexistence ID --> %',user_id USING HINT = 'Please check your user ID';
END;
/

call proc_raise2(300011);
drop procedure proc_raise2;