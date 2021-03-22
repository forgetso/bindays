var searchSteets = function (searchTerm) {
    return fetch(process.env.REACT_APP_API_URL + 'streets' + '?q=' + searchTerm.toString(),
        {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                "Accept": "application/json",
                "Access-Control-Allow-Origin": "*"
            }
        }).then((res) => {
        return res.json();
    }).then((data) => {
        return data;
    });
};
var getStreet = function (city, street) {
    return fetch(process.env.REACT_APP_API_URL + "/street/" + city + "/" + street,
        {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                "Accept": "application/json",
                "Access-Control-Allow-Origin": "*"
            }
        }).then((res) => {
        return res.json();
    }).then((data) => {
        return data;
    });
};

var getStreetsPaged = function (city, page) {
    return fetch(process.env.REACT_APP_API_URL + "/streetspaged/" + city + "/" + page,
        {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                "Accept": "application/json",
                "Access-Control-Allow-Origin": "*"
            }
        }).then((res) => {
            console.log(res);
        return res.json();
    }).then((data) => {
        return data;
    });
};

exports.searchSteets = searchSteets;
exports.getStreet = getStreet;
exports.getStreetsPaged = getStreetsPaged;
