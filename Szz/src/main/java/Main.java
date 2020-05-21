/*
 * MIT License
 *
 * Copyright (c) 2018 Axis Communications AB
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in all
 * copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 * SOFTWARE.
 */

import diff.SimplePartition;

import java.io.File;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.*;
import org.apache.commons.cli.*;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import parser.GitParserThread;
import util.Configuration;
import java.time.format.DateTimeFormatter;
import java.time.LocalDateTime;

/**
 * @author Oscar Svensson
 */
public class Main {

  private static final Logger logger = LoggerFactory.getLogger(Main.class);

  private static boolean deleteDirectory(File directoryToBeDeleted) {
    File[] allContents = directoryToBeDeleted.listFiles();
    if (allContents != null) {
      for (File file : allContents) {
        deleteDirectory(file);
      }
    }
    return directoryToBeDeleted.delete();
  }

  public static void main(String... args) {
    DateTimeFormatter dtf = DateTimeFormatter.ofPattern("HH:mm:ss");
    LocalDateTime startTime = LocalDateTime.now();
    logger.info(String.format("Started at %s", dtf.format(startTime)));
    Configuration conf = Configuration.init(logger, args);

    File toBeDeleted = Paths.get("./issues").toFile();
    deleteDirectory(toBeDeleted);

    List<String> issue_paths =
        SimplePartition.splitFile(conf.getNumberOfCPUS(), conf.getIssuePath(), "./issues");
    if (issue_paths.isEmpty()) {
      logger.warn("Empty issues");
      return;
    }

    List<GitParserThread> parsers = new LinkedList<>();
    List<String> resPaths = new LinkedList<>();
    for (int i = 0; i < conf.getNumberOfCPUS(); i++) {
      String resPath = String.format("%s/result%d", conf.getResultPath(), i);
      resPaths.add(resPath);

      parsers.add(new GitParserThread(i, issue_paths.get(i)));
      parsers.get(i).start();
    }

    for (int i = 0; i < conf.getNumberOfCPUS(); i++) {
      try {
        parsers.get(i).join();
      } catch (Exception e) {
        logger.warn(e.getMessage());
      }
    }
    logger.info("Merging files...");
    SimplePartition.mergeFiles(resPaths, conf.getResultPath());
    LocalDateTime endTime = LocalDateTime.now();
    logger.info(String.format("Done at %s",  dtf.format(endTime)));
  }
}
