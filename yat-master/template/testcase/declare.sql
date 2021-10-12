declare
c int;
begin
    c := DBMS_STATS.auto_sample_size;
    dbms_output.put_line('DBMS_STATS.AUTO_SAMPLE_SIZE'||'is'||c);
end;
/