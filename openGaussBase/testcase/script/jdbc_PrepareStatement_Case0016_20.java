"""
Copyright (c) 2022 Huawei Technologies Co.,Ltd.

openGauss is licensed under Mulan PSL v2.
You can use this software according to the terms and conditions of the Mulan PSL v2.
You may obtain a copy of Mulan PSL v2 at:

          http://license.coscl.org.cn/MulanPSL2

THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND,
EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT,
MERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.
See the Mulan PSL v2 for more details.
"""
import java.io.BufferedInputStream;
import java.io.FileInputStream;
import java.sql.*;
import java.util.ArrayList;
import java.util.Properties;

/**
 **/

public class jdbc_PrepareStatement_Case0016_20 {

    static public String driver = "org.postgresql.Driver";
	static public String tb_name ;
    public static Properties getConfigFromFile(String filePath) {
        Properties props = new Properties();
        try {
            BufferedInputStream config = new BufferedInputStream(new FileInputStream(filePath));
            props.load(config);
        } catch (Exception e) {
            e.printStackTrace();
        }
        return props;
    }

    public static String genURLFromPro(Properties props) {
        String hostname = props.getProperty("hostname");
        String[] hostnames = hostname.split(",");
        String port = props.getProperty("port");
        String[] ports = port.split(",");
        String dbname = props.getProperty("dbname");
		tb_name = props.getProperty("tbname");
        return genURLFromHostsPortsDBname(hostnames, ports, dbname);
    }

    public static String genURLFromHostsPortsDBname(String[] hostnames, String[] ports, String dbname) {
        String sourceURL;
        if (hostnames.length == 1) {
            sourceURL = "jdbc:postgresql://" + hostnames[0] + ":" + ports[0] + "/" + dbname;
        } else {
            ArrayList<String> ip_port_pare = new ArrayList<>();
            if (ports.length == 1) {
                for (String ip : hostnames) {
                    ip_port_pare.add(ip + ":" + ports[0]);
                }
            } else {
                for (int i = 0; i < hostnames.length; i++) {
                    ip_port_pare.add(hostnames[i] + ":" + ports[i]);
                }
            }
            sourceURL = "jdbc:postgresql://" + String.join(",", ip_port_pare) + "/" + dbname;
        }
        return sourceURL;
    }

    public static Connection GetConnection(Properties props) {
        Connection connR;
        String sourceURL = genURLFromPro(props);
        System.out.println(sourceURL);
        try {
            Class.forName(driver).newInstance();
            connR = DriverManager.getConnection(sourceURL, props);
        } catch (Exception var10) {
            var10.printStackTrace();
            return null;
        }
        return connR;
    }

    public static void CreateTable(Connection conn) {
        Statement stmt = null;
        try {
            stmt = conn.createStatement();
            int rc = stmt.executeUpdate("drop table if exists "+tb_name+"; "
            		+ "CREATE TABLE "+tb_name+"(c_customer_sk int,c_customer_name VARCHAR(32),c_customer_bak char(20),c_customer_bak1 char(20));");
            stmt.close();
            System.out.println("creatable succeed!");
        } catch (SQLException e) {
            if (stmt != null) {
                try {
                    stmt.close();
                } catch (SQLException e1) {
                    e1.printStackTrace();
                }
            }
            e.printStackTrace();
        }
    }

    //执行预处理语句，批量插入数据。
    public static void BatchInsertData(Connection conn) {
        PreparedStatement pst = null;
        try {
            //生成预处理语句。
            pst = conn.prepareStatement("INSERT INTO "+tb_name+" VALUES (?,?,?)");
            for (int i = 0; i < 90000; i++) {
                //添加参数。
                pst.setInt(1, i);
                pst.setString(2, "data" + i);
                pst.setString(3, "bak" + i);
                pst.addBatch();
            }
            System.out.println(" 添加参数完成!");
            //执行批处理。
            pst.executeBatch();
            pst.close();
            System.out.println("insertdata succeed!");
        } catch (SQLException e) {
            if (pst != null) {
                try {
                    pst.close();
                } catch (SQLException e1) {
                    e1.printStackTrace();
                }
            }
            e.printStackTrace();
        }
    }
    public static void main(String[] args) {
        Properties pros = new Properties();
        Properties pros_conf=null;
        String jdbc_config_file = null;
        for (int i = 0; i < args.length; i++) {
            switch (args[i]) {
                case "--config-file":
                    jdbc_config_file = args[i + 1];
                    pros_conf=getConfigFromFile(jdbc_config_file);
                    break;
                case "-F":
                    jdbc_config_file = args[i + 1];
                    pros_conf=getConfigFromFile(jdbc_config_file);
                    break;
                default:
                    break;
            }
        }
        //建立连接
        if (pros_conf!=null){
            //以参数为准，覆盖配置文件中的
            pros_conf.putAll(pros);
        }
        Connection conn = GetConnection(pros_conf);
        //创建表。
        CreateTable(conn);
        //批插数据。
        BatchInsertData(conn);
        // 查询预编译
        PreparedStatement stmt_select = null;
        try {
            //查询指定列
            stmt_select = conn.prepareStatement("select c_customer_name from  "+tb_name+" WHERE c_customer_sk =?");
            for(int i=0;i<1000;i++)
            {
                stmt_select.setInt(1, i);
                stmt_select.executeQuery();
                if (i == 0 || i == 999)
                {
                	System.out.println("select succeed!"+i);
                }
            }
            stmt_select.close();
        } catch (SQLException e) {
            e.printStackTrace();
        }
        finally {
            try {
            	stmt_select.close();
                conn.close();
            } catch (SQLException e) {
                e.printStackTrace();
            }
        }
    }
}