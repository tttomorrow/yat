-- @testpoint: INSERT语句后带优化器index，已存在的索引

insert /*+index(hint_index_000000,hint_index_00000_idx1)*/ into hint_index_00000
values ( 21, 30000, 20000, 0, 1, 30000, 294453248,  2, -110231552, 9, 'ghi',
 '2004-05-24', 'kbvumx', to_date('2010-08-08', 'yyyy-mm-dd') );
drop view if exists hint_index_000000;