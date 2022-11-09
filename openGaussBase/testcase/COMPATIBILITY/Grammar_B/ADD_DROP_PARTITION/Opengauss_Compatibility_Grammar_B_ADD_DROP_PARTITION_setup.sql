-- @testpoint: 创建表空间
drop tablespace if exists b_tbsp1;
drop tablespace if exists b_tbsp2;
drop tablespace if exists b_tbsp3;
drop tablespace if exists b_tbsp4;
drop tablespace if exists b_tbsp5;
create tablespace b_tbsp1 relative location 'b_tbsp1';
create tablespace b_tbsp2 relative location 'b_tbsp2';
create tablespace b_tbsp3 relative location 'b_tbsp3';
create tablespace b_tbsp4 relative location 'b_tbsp4';
create tablespace b_tbsp5 relative location 'b_tbsp5';
