import random
import pandas as pd
import math
import operator

"""
Fungsi min_max_scaling dibawah yaitu untuk normalisasi nilai sebuah atribut menjadi nilai skala antara 0 sampai 1
"""
def min_max_scaling(column):
    return ((column - column.min()) / (column.max() - column.min()))

"""
fungsi euclidianDistance dibawah mengambil 2 parameter dari instance data dalam range yaitu sebanyak parameter label yang dibutuhkan
sebelum mencari nilai tsb apabila ingin memfilter terlebih dahulu beberapa atribut yang diperlukan bisa melihat dibawah
"""
def euclidianDistance(data1,data2):
    distance = 0
    for i in range(len(data1)-1):
        # print(data1[i],data2[i])
        distance += (data1[i] - data2[i])**2
    return math.sqrt(distance)

"""
fungsi getNeighbors dibawah yaitu mencari tetangga terdekat dari suatu set data latih / train set, dengan membandingkan dengan data instance data test /data uji
output dari neigbor dibawah memberikan sebanyak K yang di input
"""
def getNeighbors(train_set, test_sample, k):
    distances = []
    neighbors = []

    for x in range(len(train_set)):
        dist = euclidianDistance(test_sample, train_set[x])
        distances.append((train_set[x], dist))

    distances.sort(key=operator.itemgetter(1)) #bisa tidak menggunakan library operator dan diganti dengan fungsi lambda
    #hasil list distances di sorting berdasarkan nilai euclidianDistance terkecil yang kemudian di return/output sebanyak k 
    for x in range(k):
        neighbors.append(distances[x][0])

    return neighbors 

"""
fungsi getResponse dibawah yaitu memberikan output label class voting terbanyak dari K neighbors
"""
def getResponse(neighbors):
    Votes = {}
    for i in range(len(neighbors)):
        response = neighbors[i][-1]
        if response in Votes:
            Votes[response] += 1
        else:
            Votes[response] = 1

    sortVotes = sorted(Votes.items(),key=operator.itemgetter(1),reverse=True)

    return sortVotes[0][0]

"""
Setelah mendapatkan Votes respon, bisa melihat akurasi hasil dari implementasi alogritma tsb dengan melakukan perbandingan antara data uji dan hasil prediksi
"""
def getAccuracy(testSet,predictions):
    correct = 0
    for i in range(len(testSet)):
        if testSet[i][-1] == predictions[i]:
            correct += 1
    return (correct/float(len(testSet))) * 100.0

"""
Fungi result_KNN sebagai main function sehingga bisa dipanggil berkali kali dengan merubah nilai K
"""
def result_KNN(trainSet,testSet,k):
    print(f"Jika K-{k}")
    predictions = []
    for i in range(len(testSet)):
        neigbors = getNeighbors(trainSet,testSet[i],k)
        result = getResponse(neigbors)
        predictions.append(result)
        # Jika ingin melhat aktual perbandingan data Uji dengan prediksi bisa uncomment kode dibawah
        # print(f"Prediksi {result}, Aktual {testSet[i][-1]}")
    accuracy = getAccuracy(testSet,predictions)
    accuracy = float("{:.2f}".format(accuracy))
    print("Akurasi adalah",accuracy,"%")

"""
fungsi export dibawah untuk export data mentah menjadi data set Latih / Train Set dan juga data set Uji / Tes Set
tambahan requirement menggunakan Openpyxl
#########
def exportFile(filename):
    wb = xl.Workbook()
    ws = wb.active
    for x in range(1,len(trainSet)+1):
        for y in range(1,11):
            ws.cell(row=x,column=y).value = trainSet[x-1][y-1]

    for x in range(len(trainSet)+10,len(trainSet)+len(testSet)+1):
        for y in range(1,11):
            ws.cell(row=x,column=y).value = testSet[x-len(trainSet)-11][y-1]
    wb.save(filename)

"""
#####################################################################################

"""
 ---------------------------------- Main Function ----------------------------------
"""
if __name__ == "__main__":
    # Jika ingin melakukan interactial input tanpa harus mengganti setiap saat ingin mengganti dataset baru 
    """
    FILENAME = input("Masukkan Nama File :")
    TYPE = input("Masukkan Jenis File Tsb [excel/csv]")
    if TYPE[0].lower() == 'e':
        data = pd.read_excel(f'{FILENAME}.xlsx') # disesuaikan dengan tempat folder jika file dataset terpisah
    else:
        data = pd.read_csv(f'{FILENAME}.csv')
    """

    #------------------------------------------
    """
    PERHATIAN !!!
    File Dataset dibawah digunakan asli dalam sebuah skripsi, jika memang ingin menggunakan full kode disini diharapkan menggunakan dataset lain :)
    """

    data = pd.read_excel(f'dataset/dataR2.xlsx')

    """
    Sebelum melakukan normalisasi data, jika ingin melakukan seleksi data atribut hanya yang dibutuhkan bisa melakukan seperti dibawah
    data = data[['Age', 'BMI', 'Glucose', 'Insulin', 'HOMA', 'Leptin', 'Adiponectin']]
    
    Jika memang atributnya tergolong kecil bisa langsung ke proses normalisasi
    """
    #Normalisasi Data dan Slicing Label terakhir karena sebagai Klasifikasi
    for col in data.columns[:-1]:
        data[col] = min_max_scaling(data[col])

    trainSet = []
    testSet = []
    # Loop dibawah yaitu generate secara otomatis antara Data Latih dan Data Uji, serta mencegah kesamaan data antara Data Latih dan Data Uji
    for idx,row in data.iterrows():
        dataset = [val for val in row[:-1]]
        #Mengganti index klasifikasi angka dengan variabel yang lebih mudah dibaca
        if int(row[-1]) == 1:
            label = ["Healthy Controls"]
        else:
            label = ["Patients"]
        dataset += label
        if random.random() < 0.75: # Persentase pembagian bisa disesuaikan dengan jumlah dataset, dalam kasus ini 75% data latih, 25% data uji
            trainSet.append(dataset)
        else:
            testSet.append(dataset)


    """
    # Jika ingin menampilkan semua data latih dan data uji
    print("----------------Train Set----------------------")
    for row in trainSet:
        print(row)

    print("----------------Test Set----------------------")
    for row in testSet:
        print(row)
    """

    print()
    result_KNN(trainSet,testSet,3)
    result_KNN(trainSet,testSet,5)
    result_KNN(trainSet,testSet,7)
    print("--------------------------")
    print("K yang direkomendasikan adalah Akar dari jumlah data latih")
    k = int(math.sqrt(len(trainSet)))
    if k%2 == 0: k -= 1
    print(f"Jumlah Data Latih yaitu {len(trainSet)}, sehingga akar untuk menentukan K adalah {k}")
    result_KNN(trainSet,testSet,k)
    print(f"Data Latih == {len(trainSet)}, Data Uji == {len(testSet)}")
    print()
