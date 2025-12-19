package com.bigdata;

import java.io.IOException;
import java.util.StringTokenizer;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;

/**
 * WordCount - Exemple classique de MapReduce
 * 
 * Ce programme compte le nombre d'occurrences de chaque mot dans un fichier texte.
 * 
 * Utilisation:
 *   hadoop jar wordcount-1.0.jar WordCount <input> <output>
 */
public class WordCount {

    /**
     * Mapper : Transforme chaque ligne en paires (mot, 1)
     */
    public static class TokenizerMapper extends Mapper<Object, Text, Text, IntWritable> {

        private final static IntWritable one = new IntWritable(1);
        private Text word = new Text();

        /**
         * Méthode map() appelée pour chaque ligne du fichier d'entrée
         * 
         * @param key     Position dans le fichier (ignorée ici)
         * @param value   Une ligne de texte
         * @param context Contexte pour écrire les résultats
         */
        public void map(Object key, Text value, Context context) 
                throws IOException, InterruptedException {
            
            // Découper la ligne en mots
            StringTokenizer itr = new StringTokenizer(value.toString());
            
            // Pour chaque mot
            while (itr.hasMoreTokens()) {
                String token = itr.nextToken();
                
                // Nettoyer le mot (enlever la ponctuation, mettre en minuscules)
                token = token.replaceAll("[^a-zA-Z0-9àâäéèêëïîôùûüÿçÀÂÄÉÈÊËÏÎÔÙÛÜŸÇ]", "").toLowerCase();
                
                // Ignorer les mots vides
                if (token.length() > 0) {
                    word.set(token);
                    // Émettre (mot, 1)
                    context.write(word, one);
                }
            }
        }
    }

    /**
     * Reducer : Additionne toutes les occurrences pour chaque mot
     */
    public static class IntSumReducer extends Reducer<Text, IntWritable, Text, IntWritable> {
        
        private IntWritable result = new IntWritable();

        /**
         * Méthode reduce() appelée pour chaque mot unique
         * 
         * @param key     Le mot
         * @param values  Liste de tous les compteurs (1, 1, 1, ...)
         * @param context Contexte pour écrire les résultats
         */
        public void reduce(Text key, Iterable<IntWritable> values, Context context) 
                throws IOException, InterruptedException {
            
            int sum = 0;
            
            // Additionner toutes les occurrences
            for (IntWritable val : values) {
                sum += val.get();
            }
            
            result.set(sum);
            // Émettre (mot, nombre_total)
            context.write(key, result);
        }
    }

    /**
     * Point d'entrée du programme
     */
    public static void main(String[] args) throws Exception {
        
        // Vérifier les arguments
        if (args.length != 2) {
            System.err.println("Usage: WordCount <input path> <output path>");
            System.exit(-1);
        }

        // Créer la configuration Hadoop
        Configuration conf = new Configuration();
        
        // Créer le job
        Job job = Job.getInstance(conf, "word count");
        job.setJarByClass(WordCount.class);
        
        // Définir les classes Mapper et Reducer
        job.setMapperClass(TokenizerMapper.class);
        job.setCombinerClass(IntSumReducer.class);  // Optimisation : pré-agrégation locale
        job.setReducerClass(IntSumReducer.class);
        
        // Définir les types de sortie
        job.setOutputKeyClass(Text.class);
        job.setOutputValueClass(IntWritable.class);
        
        // Définir les chemins d'entrée et de sortie
        FileInputFormat.addInputPath(job, new Path(args[0]));
        FileOutputFormat.setOutputPath(job, new Path(args[1]));
        
        // Lancer le job et attendre la fin
        System.exit(job.waitForCompletion(true) ? 0 : 1);
    }
}
