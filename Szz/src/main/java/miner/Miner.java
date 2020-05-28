package miner;

import gr.uom.java.xmi.diff.CodeRange;
import gr.uom.java.xmi.diff.ExtractOperationRefactoring;
import org.eclipse.jgit.lib.Repository;
import org.refactoringminer.api.GitHistoryRefactoringMiner;
import org.refactoringminer.api.Refactoring;
import org.refactoringminer.api.RefactoringHandler;
import org.refactoringminer.rm1.GitHistoryRefactoringMinerImpl;

import java.util.HashMap;
import java.util.LinkedList;
import java.util.List;
import java.util.Map;

public class Miner {
    static private final GitHistoryRefactoringMiner miner = new GitHistoryRefactoringMinerImpl();

    static private final Map<String, Map<String, List<Integer>>> cache = new HashMap<>();
    static public Map<String, List<Integer>>getRefactoringLines(Repository repo, String sourceHash) throws Exception {
        if (!cache.containsKey(sourceHash)) {
            cache.put(sourceHash, getRefactoringLinesWithoutCache(repo, sourceHash));
        }
        return cache.get(sourceHash);
    }

    static private Map<String, List<Integer>> getRefactoringLinesWithoutCache(Repository repo, String sourceHash) throws Exception {
        Map<String, List<Integer>> refLinesMap = new HashMap<>();
        miner.detectAtCommit(repo,
            sourceHash,
            new RefactoringHandler() {
                @Override
                public void handle(String commitId, List<Refactoring> refactorings) {
                    for (Refactoring ref : refactorings) {
                        handleRefactoring(ref, refLinesMap);
                    }
                }
            });
        return refLinesMap;
    }

    static private void handleRefactoring(Refactoring refactoring, Map<String, List<Integer>> rlm) {
        refactoring.rightSide().forEach(cr -> handleCodeRange(cr, rlm));
    }

    static private void handleCodeRange(CodeRange codeRange, Map<String, List<Integer>> refLinesMap) {
        if (!refLinesMap.containsKey(codeRange.getFilePath())) {
            refLinesMap.put(codeRange.getFilePath(), new LinkedList<>());
        }
        List<Integer> lines = refLinesMap.get(codeRange.getFilePath());
        for (int i = codeRange.getStartLine(); i <= codeRange.getEndLine(); i++) {
            lines.add(i);
        }
    }
}
