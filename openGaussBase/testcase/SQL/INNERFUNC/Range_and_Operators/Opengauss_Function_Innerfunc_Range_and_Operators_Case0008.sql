-- @testpoint: isempty(anyrange) 描述：范围是否为空,无效入参时，合理报错

select isempty(macaddr('08:00:2b:01:02:03'::macaddr ,'08:00:2b:01:02:03'::macaddr)) as result;
create type bugstatus as enum ('create', 'modify', 'closed');
drop type bugstatus;
select isempty(bugstatus (create, closed)) as result;
select isempty(uuid('a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11'::uuid,'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a22'::uuid)) as result;