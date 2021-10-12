@comment
{
    propers: xxxx
    目的： 休息休息
    XMDS asd
    fas
    dynamic_function asdf ( ) { \}
    \\xa

}

@setup
{
    create table xa_tb(id int);
}

@test
{
    select * from xa_tb;
}

@expect {
    id
    --
    1
    2
    3
    4
}

@cleanup
{
    drop table xa_tb;
}