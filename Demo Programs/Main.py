import QuickSort
import MergeSort
import InsertionSort
import SelectionSort

if __name__ == '__main__':
    l = [2, 7, 3, 1, 0, 11, 9, 8]
    QuickSort.quickSort(l)
    MergeSort.mergeSort(l)
    InsertionSort.insertionSort(l)
    SelectionSort.selectionSort(l)
    print(l)