--  @testpoint:序列名称测试
--序列名由大写字母，小写字母，数字，特殊字符组成
drop SEQUENCE if exists Test#seq1;
create SEQUENCE Test#seq1;
--序列名由大写字母，小写字母，数字,%，-组成，合理报错
create SEQUENCE Test%seq1;
create SEQUENCE Test-seq2;
--删除序列
drop SEQUENCE Test#seq1;