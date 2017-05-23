/**
 * Created by lc on 2017-05-22.
 */

$(function () {
    'use strict';

    var main = $('#paint');

    function reset() {
        main.clearCanvas();
    }

    main.css('background-color', '#ccc');

    function Scenario() {
        if (!this instanceof Scenario) {
            return new Scenario();
        }

        this.points = [];
        this.gimmicks = {};
        this.playerPos = {x: 0, y: 0};
        this.playerRadius = {};
        this.playerSpeed = 0;

        this.update = function () {
            reset();
            for (var key in this.gimmicks) {
                if (!this.gimmicks.hasOwnProperty(key)) {
                    continue;
                }
                for (var i = 0, n = this.gimmicks[key].length; i < n; ++i) {
                    var obj = this.gimmicks[key][i];
                    drawGimmick(key, obj.x1, obj.y1, obj.x2, obj.y2);
                }
            }

            for (i = 0, n = this.points.length; i < n; ++i) {
                drawPoint(this.points[i].x, this.points[i].y);
            }


            drawBall(this.playerPos.x, this.playerPos.y);
        };

        this.processData = function (message) {
            var data = message.split(';'); // keeping it as string is perfectly fine
            this.playerPos = {x: data[0], y: data[1]};
            // in order: red, blue, yellow, green
            var i = 2;
            var gm_kind = ['red', 'blue', 'yellow', 'green'];
            for (var g = 0; g < 4; ++g) {
                var temp = [];
                while (data[i]) {
                    temp.push({x1: data[i], y1: data[i + 1], x2: data[i + 2], y2: data[i + 3]});
                    i += 4;
                }
                ++i;
                this.gimmicks[gm_kind[g]] = temp;
            }
            this.points = [];
            while (data[i]) {
                this.points.push({x: data[i], y: data[i + 1]});
                i += 2;
            }
            this.update();
        };
    }

    function drawGimmick(type, x1, y1, x2, y2) {
        return main.drawLine({
            x1: x1, y1: y1,
            x2: x2, y2: y2,
            strokeWidth: 5,
            strokeStyle: type
        });
    }

    function drawPoint(x, y) {
        return main.drawEllipse({
            x: x, y: y,
            width: 10, height: 10,
            fillStyle: 'white'
        })
    }

    function drawBall(x, y) {
        return main.drawEllipse({
            x: x, y: y,
            width: 30, height: 30,
            strokeStyle: 'black',
            strokeWidth: 2
        })
    }


    //
    // drawGimmick('blue', 10, 10, 30, 30);
    // drawBall(300, 360);
    // drawPoint(400, 400);
    // reset();

    //split parameters
    var path = window.location.search.substring(1);

    // connect
    var manager = new Scenario();
    var socket = new WebSocket('ws://' + window.location.host);
    socket.onopen = function () {
        this.send(path);
    };
    socket.onmessage = function (message) {
        console.log(message.data);
        manager.processData(message.data);
    };
    if (socket.readyState === WebSocket.OPEN) {
        socket.onopen(); // late trigger
    }
});