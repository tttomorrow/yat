-- @testpoint: 删除表中数据
DROP TABLE IF EXISTS reason_t2;
CREATE TABLE reason_t2
(
  r_reason_sk    integer,
  r_reason_id character(16),
  r_reason_desc  character(100)
);
INSERT INTO reason_t2 VALUES (3, 'AAAAAAAACAAAAAAA','reason3'),(4, 'AAAAAAAADAAAAAAA', 'reason4'),(5, 'AAAAAAAAEAAAAAAA','reason5');
delete from  reason_t2;
DROP TABLE IF EXISTS reason_t2;