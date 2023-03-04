# Spoofing Detection on Factory I/O
Modbus packet spoofing using unsupervised machine learning on Factory I/O

## Setup
Instructionas assume a Windows 10 setup with WSL. Factory I/O only runs on Windows

### 1. Install VirtualBox
Install [VirtualBox](https://www.virtualbox.org/wiki/Downloads) for Windows

### 2. Install Factory I/O
Install [Factory I/O](https://factoryio.com/). This will require a valid license.

### 3. Host Only Network
Create the following host only network
```192.168.56.0/24```

### 4. Virtual Machines
We use three virtual machines as part of the VM topology. All of them run [Debian GNU/Linux](https://www.debian.org/). Download the prebuilt VMs and add them to the host only network.

**Prebuilt VMs**
* [factoryio_plc](https://csuohio-my.sharepoint.com/:u:/g/personal/2691149_vikes_csuohio_edu/EYCisnDWMSBJqz4v0Z1-RxsBCBdJfsBR2TdHj-R5N9z9cQ?e=Fe3377)
* [factoryio_hmi](https://csuohio-my.sharepoint.com/:u:/g/personal/2691149_vikes_csuohio_edu/EegklZsoKo5Mlvm97hMyzPYBtOYA0mK9P4fhhPa-6rRUAA?e=bYtof2)
* [factoryio_attacker](https://csuohio-my.sharepoint.com/:u:/g/personal/2691149_vikes_csuohio_edu/EYV-v-ijEOFDmxcOG6TlXtMBUsiKnn9WXmk5jdOrYrV45w?e=bjvDwg)

**Shared Folders**
* Create a shared folder between the data-capture directory and /home/hmi/data-capture on the factoryio_hmi VM
* Create a shared folder between the modbus-attacks directory and /home/attacker/modbus-attacks on the factoryio_attacker VM

### 5. Download Production Line Scene
Download the [Production Line](https://openplc.discussion.community/post/production-line-scene-from-factory-io-fbd-11657885) scene with renamed variables. Import the scene into Factory I/O and rename it to Production Line

### 6. Fix Paths in Scripts
In capture-training-data.sh, capture-attack-data.sh, capture-benign-data.sh, and live-monitor.sh, replace all instances of <user> with the appropriate username

### 7. Install Host Machine Dependencies
Install the required python libraries
```
pip3 install -r requirements.txt
```

## Running the Experiment
### Create Snapshot
This will create a snapshot of all VMs in a booted state. Each time the machines are booted, the state is restored to this snapshot.
```
bash create-snapshot.sh
```
### Capturing Training Data
This will capture a full cycle (400 seconds) of benign data.
```
bash capture-training-data.sh
```
### Training the Model
This will train the model using the training data previously captured.
```
python3 train.py
```
### Capturing Attack Data
This will capture attack data for all 7 attacks. Each attack is run for a full cycle (400 seconds).
```
bash capture-attack-data.sh
```
### Capture Benign Data
This will capture 50 cycles (roughly 5.5 hours worth) of benign data to verify that the model does not induce any false positives.
```
bash capture-benign-data.sh
```
### Testing the model
This will test the model against all the attack and benign datasets.
```
python3 batch.py
```
### Detection Time
This will collect the detection time for each attack and log it to a file time.csv. Each attack is only run for a full cycle (400 seconds).
```
bash detection-time.sh
```
