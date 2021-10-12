-- @testpoint: 创建同义词为关键字，保留关键字，作为同义词名称，合理报错
--创建同义词为保留关键字，合理报错
drop synonym if EXISTS ALL cascade;
drop synonym if EXISTS NULL cascade;
drop synonym if EXISTS for cascade;
drop synonym if EXISTS create cascade;
drop synonym if EXISTS select cascade;
drop synonym if EXISTS table cascade;
drop synonym if EXISTS function cascade;
drop synonym if EXISTS in cascade;
drop synonym if EXISTS PROCEDURE cascade;
drop synonym if EXISTS true cascade;
drop synonym if EXISTS false cascade;
drop synonym if EXISTS else cascade;
drop synonym if EXISTS FOR cascade;
create synonym ALL for test_synonym;
create synonym NULL for test_synonym;
create synonym create for test_synonym;
create synonym create for test_synonym;
create synonym select for test_synonym;
create synonym table for test_synonym;
create synonym in for test_synonym;
create synonym PROCEDURE for test_synonym;
create synonym true for test_synonym;
create synonym false for test_synonym;
create synonym else for test_synonym;
create synonym for for test_synonym;
--非保留关键字，成功
create synonym function for test_synonym;
drop synonym if EXISTS drop cascade;
drop synonym if EXISTS update cascade;
drop synonym if EXISTS delete cascade;
drop synonym if EXISTS insert cascade;
drop synonym if EXISTS index cascade;
drop synonym if EXISTS sequence cascade;
drop synonym if EXISTS if cascade;
drop synonym if EXISTS TRIGGER cascade;
drop synonym if EXISTS CURSOR cascade;
drop synonym if EXISTS between cascade;
drop synonym if EXISTS int cascade;
drop synonym if EXISTS public cascade;
drop synonym if EXISTS cascade cascade;
drop synonym if EXISTS begin cascade;
create synonym drop for test_synonym;
create synonym update for test_synonym;
create synonym delete for test_synonym;
create synonym insert for test_synonym;
create synonym index for test_synonym;
create synonym sequence for test_synonym;
create synonym TRIGGER for test_synonym;
create synonym if for test_synonym;
create synonym CURSOR for test_synonym;
create synonym between for test_synonym;
create synonym int for test_synonym;
create synonym public for test_synonym;
create synonym cascade for test_synonym;
create synonym begin for test_synonym;
--清理环境
drop synonym if EXISTS drop cascade;
drop synonym if EXISTS update cascade;
drop synonym if EXISTS delete cascade;
drop synonym if EXISTS insert cascade;
drop synonym if EXISTS index cascade;
drop synonym if EXISTS sequence cascade;
drop synonym if EXISTS if cascade;
drop synonym if EXISTS TRIGGER cascade;
drop synonym if EXISTS CURSOR cascade;
drop synonym if EXISTS between cascade;
drop synonym if EXISTS int cascade;
drop synonym if EXISTS public cascade;
drop synonym if EXISTS cascade cascade;
drop synonym if EXISTS begin cascade;
drop synonym if EXISTS function cascade;













