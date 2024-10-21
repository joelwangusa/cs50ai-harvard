import csv
import sys

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """
    months = {"Jan": 0, "Feb": 1, "Mar": 2, "Apr": 3,
              "May": 4, "June": 5, "Jul": 6, "Aug": 7,
              "Sep": 8, "Oct": 9, "Nov": 10, "Dec": 11
              }
   
    with open(filename) as f:
        reader = csv.reader(f)
        # Get CSV Columns
        columns = next(reader)
        evidence, labels = [], []
        for row in reader:
            # build evidence for current row
            e = []
            for i, cell in enumerate(row[:-1]):
                # Int values
                if columns[i] in ["Administrative", "Informational", "ProductRelated",
                                  "OperatingSystems", "Browser", "Region"]:
                    # Handle Int values
                    e.append(int(cell))
                elif columns[i] == "Month":
                    # Handle Month
                    e.append(months[cell])
                elif columns[i] == "VisitorType":
                    # Handle Visitor Type
                    if cell == "Returning_Visitor":
                        e.append(1)
                    else:
                        e.append(0)
                elif columns[i] == "Weekend":
                    # Handle Weekend
                    if cell == "TRUE":
                        e.append(1)
                    else:
                        e.append(0)
                else:
                    # Handle float values
                    e.append(float(cell))

            # build label for current row
            l = 1 if row[-1] == "TRUE" else 0

            evidence.append(e)
            labels.append(l)
    
    return (evidence, labels)


def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    model = KNeighborsClassifier(n_neighbors=1)
    # Fit model
    model.fit(evidence, labels)
    
    return model


def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificity).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    # Sensitivity
    actual_positive, total_positive_predict = 0, 0
    actual_negative, total_negative_predict = 0, 0
    N = len(predictions)
    for i in range(N):
        prediction = predictions[i]
        label = labels[i]
        if label == 1:
            total_positive_predict += 1
            if prediction == label:
                actual_positive += 1
        else:
            total_negative_predict += 1
            if prediction == label:
                actual_negative += 1
    
    sensitivity = actual_positive / total_positive_predict
    specificity = actual_negative / total_negative_predict

    return sensitivity, specificity


if __name__ == "__main__":
    main()
