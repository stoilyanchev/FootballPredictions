/**
 * Copyright 2012 Neuroph Project http://neuroph.sourceforge.net
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *    http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

package predictingtheresultoffootballmatch;

import java.io.FileNotFoundException;
import java.io.IOException;
import java.util.Arrays;
import java.util.logging.Level;
import java.util.logging.Logger;
import org.neuroph.core.NeuralNetwork;
import org.neuroph.core.learning.DataSet;
import org.neuroph.core.learning.DataSetRow;
import org.neuroph.nnet.MultiLayerPerceptron;
import org.neuroph.nnet.learning.MomentumBackpropagation;
import org.neuroph.util.TrainingSetImport;
import org.neuroph.util.TransferFunctionType;

/**
 *
 * @author Ivana Lukic
 */
public class PredictingTheResultofFootballMatch {

    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) {

        try {
            Process p = Runtime.getRuntime().exec("python ./sets.py");
        } catch (IOException ex) {
            Logger.getLogger(PredictingTheResultofFootballMatch.class.getName()).log(Level.SEVERE, null, ex);
        }
        
        String trainingSetFileName = "set.txt";
        int inputsCount = 12;
        int outputsCount = 3;
        

        System.out.println("Running Sample");
        System.out.println("Using training set " + trainingSetFileName);

        // create training set
        DataSet trainingSet = null;
        try {
            trainingSet = TrainingSetImport.importFromFile(trainingSetFileName, inputsCount, outputsCount, " ");
        } catch (FileNotFoundException ex) {
            System.out.println("File not found!");
        } catch (IOException | NumberFormatException ex) {
            System.out.println("Error reading file or bad number format!");
        }


        // create multi layer perceptron
        System.out.println("Creating neural network");
        MultiLayerPerceptron neuralNet = new MultiLayerPerceptron(TransferFunctionType.SIGMOID, 12, 30, 3);
        
                
        // set learning parametars
        MomentumBackpropagation learningRule = (MomentumBackpropagation) neuralNet.getLearningRule();
        learningRule.setLearningRate(0.3);
        learningRule.setMomentum(0.7);

        // learn the training set
        System.out.println("Training neural network...");
        neuralNet.learn(trainingSet);
        System.out.println("Done!");

        // test perceptron
        System.out.println("Testing trained neural network");
        //testPredictingTheResultofFootballMatch(neuralNet, trainingSet);
        
        String testSet = "upcoming.txt";
        DataSet resultSet = null;
        try {
            resultSet = TrainingSetImport.importFromFile(testSet, inputsCount, outputsCount, " ");
        } catch (FileNotFoundException ex) {
            System.out.println("File not found!");
        } catch (IOException | NumberFormatException ex) {
            System.out.println("Error reading file or bad number format!");
        }
        
        System.out.println("nashto\n\n\n");
        testPredictingTheResultofFootballMatch(neuralNet, resultSet);
    }

    public static void testPredictingTheResultofFootballMatch(NeuralNetwork nnet, DataSet dset) {

        for (DataSetRow trainingElement : dset.getRows()) {

            nnet.setInput(trainingElement.getInput());
            nnet.calculate();
            double[] networkOutput = nnet.getOutput();
            //System.out.print("Input: " + Arrays.toString(trainingElement.getInput()));
            //System.out.println(" Output: " + Arrays.toString(networkOutput));
            System.out.println(" Output: " + String.format("%.3f  %.3f  %.3f", networkOutput[0], networkOutput[1], networkOutput[2]));
            
            if (networkOutput[0] > networkOutput[1] && networkOutput[0] > networkOutput[2])
                System.out.println("Result: Home team wins!!!");
            else if (networkOutput[1] > networkOutput[0] && networkOutput[1] > networkOutput[2])
                System.out.println("Result: Draw!!!");
            else
                System.out.println("Result: Away team wins!!!");
        }

    }
}