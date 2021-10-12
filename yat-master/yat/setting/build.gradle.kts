import java.nio.file.Paths
import java.time.LocalDateTime
import java.time.format.DateTimeFormatter

plugins {
    kotlin("jvm")
}

dependencies {
    compileOnly("org.projectlombok:lombok:1.18.6")
    annotationProcessor("org.projectlombok:lombok:1.18.6")
    implementation(project(":yat:common"))
    implementation(project(":yat:vfs"))
    implementation(project(":yat:schedule-parser"))
    implementation("com.beust:jcommander:1.81")
    implementation("org.yaml:snakeyaml:1.29")
    implementation("org.jetbrains.kotlin:kotlin-stdlib-jdk8")
    implementation("org.jetbrains.kotlin:kotlin-reflect")

    testImplementation("org.junit.jupiter:junit-jupiter-api:5.8.0")
    testRuntimeOnly("org.junit.jupiter:junit-jupiter-engine:5.8.0")
}

tasks {
    jar {
        archiveBaseName.set("yat-${project.name}")
    }

    test {
        useJUnitPlatform()
    }

    register("writeVersion") {
        val versionPath = Paths.get(projectDir.getAbsolutePath(), "src", "main", "kotlin", "com", "huawei", "gauss", "yat", "setting", "Version.kt").toFile()
        val lines = mutableListOf<String>()
        versionPath.reader().forEachLine {
            if (it.contains("private const val YAT_VERSION_MARK = ")) {
                lines.add("    private const val YAT_VERSION_MARK = \"$project.version\";")
            } else if (it.contains("private const val YAT_BUILD_TIME_MARK = ")) {
                val now = LocalDateTime.now().format(DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss"))
                lines.add("    private const val YAT_BUILD_TIME_MARK = \"$now\";")
            } else {
                lines.add(it)
            }
        }

        versionPath.writeText(lines.joinToString("\n"))
    }
}

tasks.getByName("classes").dependsOn("writeVersion")

