-- @testpoint: 操作符&，bit和bit varying 位数不一致,合理报错
SELECT B'1111100011' & B'10101' AS RESULT;