import java.util.regex.Pattern

plugins {
    groovy
    java
    kotlin("jvm") version "1.5.30"
    id("org.hidetake.ssh") version "2.10.1"
    id("org.ajoberstar.grgit") version "4.1.0"
}

allprojects {
    repositories {
        maven {
            url = uri("https://plugins.gradle.org/m2")
            name = "Huawei Maven Mirror"
            isAllowInsecureProtocol = true
        }
        maven {
            url = uri("https://plugins.gradle.org/m2")
            name = "Maven Central"
        }
        mavenCentral()
    }

    tasks.withType<org.jetbrains.kotlin.gradle.tasks.KotlinCompile>().all {
        kotlinOptions {
            jvmTarget = "1.8"
        }
    }

    tasks.withType<JavaCompile>().all {
        sourceCompatibility = "1.8"
        targetCompatibility = "1.8"

        options.isIncremental = true
        options.compilerArgs.add("-Werror")
        options.compilerArgs.add("-Xlint:deprecation")
        options.compilerArgs.add("-Xlint:unchecked")
    }

    group = "com.huawei.gauss.yat"
    version = "0.10.26"
}

subprojects {
    rootProject.tasks.getByName("clean").dependsOn(tasks.matching { it.name == "clean" })
}

dependencies {
    implementation("org.springframework.boot:spring-boot-loader:2.5.4")
    implementation(project("yat:framework"))
}

fun findWithName(paths: Iterator<File>, name: String): String {
    for (path in paths) {
        if (Pattern.matches(name, path.toString())) {
            return path.toString()
        }
    }

    throw RuntimeException("can not found the given name: $name")
}

tasks {
    jar {
        manifest {
            attributes["Main-Class"] = "com.huawei.gauss.yat.launcher.YatLauncher"
            attributes["Start-Class"] = "com.huawei.gauss.yat.MainKt"
        }

        from(configurations.runtimeClasspath) {
            into("YAT-INF/lib")
            exclude("*spring-boot-loader*.jar")
        }

        from(
            fileTree(
                findWithName(configurations.runtimeClasspath.get().files.iterator(), ".*spring-boot-loader.*\\.jar\$")
            ).map { zipTree(it) })

        entryCompression = ZipEntryCompression.STORED
    }

    register("copyYatLauncherScript", Copy::class) {
        from("bin/yat")
        into("pkg/bin")
    }

    register("copyInstall", Copy::class) {
        from("bin/install")
        into("pkg")
    }

    register("copyDrivers", Copy::class) {
        from("driver")
        into("pkg/lib")
    }

    register("copyJars", Copy::class) {
        dependsOn("build")
        from(getByName<Jar>("jar").archiveFile)
        into("pkg/app")
    }

    register("cleanPack", Delete::class) {
        dependsOn("clean")
        delete("pkg")
    }

    register("copyTemplate", Copy::class) {
        from("template")
        into("pkg/template")
    }

    register("copyScripts", Copy::class) {
        from("script")
        into("pkg/script")
    }

    register("copyPyModule", Copy::class) {
        from("pymodule")
        into("pkg/python")
    }

    register("pack", Tar::class) {
        dependsOn(
            "copyJars", "copyYatLauncherScript", "copyInstall", "copyPyModule",
            "copyDrivers", "copyTemplate", "copyScripts"
        )

        from("pkg")
        exclude("**/*.idea", "**/*.git", "**/*.vscode", "**/*.pyc", "**/__pycache__")
        compression = Compression.GZIP

        eachFile {
            if (name == "yat" || name == "install") {
                mode = 0x1ed
            }
        }
        into("yat-${project.version}")
        destinationDirectory.set(file("archive"))
    }

    val testService = org.hidetake.groovy.ssh.core.Remote(
        mapOf(
            "user" to "root",
            "host" to "",
            "password" to ""
        )
    )


    val publishServer = org.hidetake.groovy.ssh.core.Remote(
        mapOf(
            "user" to "root",
            "host" to "",
            "password" to ""
        )
    )

    register("deployTest") {
        dependsOn("pack")

        doLast {
            ssh.run(delegateClosureOf<org.hidetake.groovy.ssh.core.RunHandler> {
                session(testService, delegateClosureOf<org.hidetake.groovy.ssh.session.SessionHandler> {
                    execute("cd /tmp; rm -rf yat*")
                    put(hashMapOf("from" to "$projectDir/archive/yat-${version}.tgz", "into" to "/tmp"))
                    execute("cd /tmp; tar xf yat-${version}.tgz; cd yat-$version; ./install -F")
                })
            })
        }
    }

    register("makeDoc") {
        doLast {
            exec {
                commandLine("mkdocs", "build")
            }
        }
    }

    register("publishDoc") {
        dependsOn("makeDoc")

        doLast {
            ssh.run(delegateClosureOf<org.hidetake.groovy.ssh.core.RunHandler> {
                session(publishServer, delegateClosureOf<org.hidetake.groovy.ssh.session.SessionHandler> {
                    execute("cd /var/www/html/static/html && rm -rf yat && mkdir -p yat")
                    put(hashMapOf("from" to "$projectDir/site", "into" to "/var/www/html/static/html/yat"))
                    execute("cd /var/www/html/static/html && mv yat/site/* yat")
                })
            })
        }
    }

    register("publish") {
        dependsOn("pack")

        doLast {
            ssh.run(delegateClosureOf<org.hidetake.groovy.ssh.core.RunHandler> {
                session(publishServer, delegateClosureOf<org.hidetake.groovy.ssh.session.SessionHandler> {
                    execute("mkdir -p /var/www/html/package/Yat")
                    put(
                        hashMapOf(
                            "from" to "$projectDir/archive/yat-${version}.tgz",
                            "into" to "/var/www/html/package/Yat"
                        )
                    )
                    execute("cd /var/www/html/package/Yat; ln -s -f yat-${version}.tgz yat-latest.tgz")
                })
            })
        }
    }
}

defaultTasks("pack")
