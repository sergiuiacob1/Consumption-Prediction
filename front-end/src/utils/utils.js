const parseCSVData = (parsedCSV) => {
    const predictModelData = {};
    //fill predictModel with keys and values;
    parsedCSV.data[0].forEach((key, index) => {
      predictModelData[key] = [];
      parsedCSV.data.forEach((array, jindex) => {
        if (jindex === 0) return;
        if (array[index]) {
          predictModelData[key].push(array[index]);
        }
      });
    });

    return predictModelData;
  }

  export default { parseCSVData };
