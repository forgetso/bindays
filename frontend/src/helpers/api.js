var baseUrl = "http://" + process.env.REACT_APP_API_HOST + ":" + process.env.REACT_APP_API_PORT
var searchSteets = function (searchTerm) {
    return fetch(baseUrl + '/streets' + '?q=' + searchTerm.toString(),
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
    return fetch(baseUrl + "/street/" + city + "/" + street,
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
    return fetch(baseUrl + "/streetspaged/" + city + "/" + page,
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
