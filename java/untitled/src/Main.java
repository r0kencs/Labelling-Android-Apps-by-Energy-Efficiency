import org.jf.dexlib2.DexFileFactory;
import org.jf.dexlib2.Opcode;
import org.jf.dexlib2.Opcodes;
import org.jf.dexlib2.iface.ClassDef;
import org.jf.dexlib2.iface.DexFile;
import org.jf.dexlib2.immutable.ImmutableDexFile;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

public class Main {

    public static void printUsage() {
        System.out.println("Usage: apkMinify path -o outputPath -i [classesToIgnore...]");
    }

    public static void main(String[] args) {
        int api = 19;

        if (args.length < 1) { printUsage(); return; }

        if (!args[1].equals("-o")) { printUsage(); return; }
        if (!args[3].equals("-i")) { printUsage(); return; }

        String path = args[0];
        String outputPath = args[2];

        List<String> ignoreNames = new ArrayList<>();
        for (int i = 4; i < args.length; i++) {
            ignoreNames.add(args[i]);
        }

        try {
            DexFile dexFile = DexFileFactory.loadDexFile(path, Opcodes.forApi(api));

            List<ClassDef> classes = new ArrayList<ClassDef>();

            for (ClassDef classDef : dexFile.getClasses()) {
                String aux = classDef.getType();
                int ignoreCounter = 0;

                for (String ignoreName : ignoreNames) {
                    if (aux.startsWith(ignoreName)) ignoreCounter++;
                }

                if (ignoreCounter == 0) classes.add(classDef);
            }

            dexFile = new ImmutableDexFile(Opcodes.forApi(api), classes);
            DexFileFactory.writeDexFile(outputPath, dexFile);

        } catch (IOException e) {
            throw new RuntimeException(e);
        }
    }
}