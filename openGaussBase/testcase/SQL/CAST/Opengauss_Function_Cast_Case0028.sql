-- @testpoint: json、txid_snapshot、sys_refcursor或几何类型进行union：合理报错

--testpoint:进行union：合理报错
explain performance SELECT row_to_json(row(1,'foo')) union SELECT row_to_json(row(1,'foo'));

--txid_snapshot:进行union：合理报错
explain performance select txid_current_snapshot() union select txid_current_snapshot();

--几何类型:进行union：合理报错
explain performance select point '1,2' union select lseg '1,2,3,2';
explain performance select box '(1,1),(2,2)' union select path '1,1,2,2,3,3,4,4';
explain performance select polygon '1,1,2,2,3,3,4,4' union select circle '1,1,5';

--清理环境
--no need to clean