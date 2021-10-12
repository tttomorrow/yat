-- @testpoint: upper_inc(anyrange) 描述：是否包含上界,入参为无效值时，合理报错

select upper_inc(macaddr('08:00:2b:01:02:03'::macaddr ,'08:00:2b:01:02:03'::macaddr)) as result;
create type bugstatus as enum ('create', 'modify', 'closed');
drop type bugstatus;
select upper_inc(bugstatus (create, closed)) as result;
select upper_inc(uuid('(a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11,a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a22)'::uuid)) as result;