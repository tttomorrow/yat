conn xxx/passwd@127.0.0.1:9090;

insert into tbl_x values(1, 2, 4);
insert into tbl_x values(3, 4, 5);

select * from tbl_x;

\! common/abc -x -p;

shell command/xml_parser -t data/abc.xml;

create or replace procedure proc_001 as
    v1 := 1
    v2 := 2
begin

    select * from xml_tbl where id == v1;
    .....
end;
/

async(timeout: 3s)
{
    set autocommit false;
    select * from tbl_x for update;
    ...
    commit;
}

select * from tbl_x;


session(name: s1)
{
    set autocommit false;
    update table tbl_x set par1 = 2 par2 = 2;
    insert into tbl_x values(1, 3, 4);
    commit;
}

session(name: s2, user: abc, password: '')
{
    set autocommit false;
    update table tbl_x set par1 = 2 par2 = 2;
    insert into tbl_x values(1, 3, 4);
    step
    {
        select * from tbl_x for update;
        select * from tbl_x;
    }
    commit;
}

execute s1.0 s2.0 s1.1 s1.2 s2.2 s2.1;

execute s1.0 s2.0 s2.1 s2.2 s1.2 s1.1;
