
const fetchService = (url, method, body, headers) => {
  const fetchParams = [];

  fetchParams.push(url);

  if (method === 'POST') {
    let fetchData = {
      method,
      body: JSON.stringify(body),
    };

    if (headers) {
      fetchData = { ...fetchData, headers };
    }
    fetchParams.push(fetchData);
  }

  return fetch(...fetchParams)
    .then((resp) => resp.json()) // Transform the data into json
}

export default fetchService
