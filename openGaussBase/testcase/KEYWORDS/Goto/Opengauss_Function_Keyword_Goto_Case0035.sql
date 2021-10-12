-- @testpoint: opengauss关键字Goto(非保留)，作为控制语句

CREATE OR REPLACE PROCEDURE GOTO_test_35()
AS
DECLARE
    v1  int;
BEGIN
    v1  := 0;
        LOOP
        EXIT WHEN v1 > 100;
                v1 := v1 + 2;
                if v1 > 25 THEN
                        GOTO pos1;
                END IF;
        END LOOP;
<<pos1>>
v1 := v1 + 10;
raise info 'v1 is %. ', v1;
END;
/

call GOTO_test_35();

--清理环境
drop PROCEDURE if exists GOTO_test_35;

