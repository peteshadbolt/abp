var ngbh = {};
var vops = {};
var meta = {};

function add_node(node, m) {
    ngbh[node] = {};
    vops[node] = clifford.hadamard;
    meta[node] = m ? m : {};
}

function add_nodes(nodes) {
    nodes.forEach(add_node);
}

function add_edge(a, b) {
    ngbh[a][b] = true;
    ngbh[b][a] = true;
}

function add_edges(edges) {
    edges.forEach(function(e) {
        add_edge(e[0], e[1]);
    });
}

function del_edge(a, b) {
    delete ngbh[a][b];
    delete ngbh[b][a];
}

function has_edge(a, b) {
    return Object.prototype.hasOwnProperty.call(ngbh[a], b);
}

function toggle_edge(a, b) {
    if (has_edge(a, b)) {
        del_edge(a, b);
    } else {
        add_edge(a, b);
    }
}

function get_swap(node, avoid) {
    for (var i in ngbh[node]) {
        if (i != avoid) {return i;}
    }
    return avoid;
}

function remove_vop(node, avoid) {
    var swap_qubit = get_swap(node, avoid);
    var decomposition = decompositions[vops[node]];
    for (var i=decomposition.length-1; i >=0; --i) {
        var v = decomposition[i];
        local_complementation(v == "x" ? a : swap_qubit);
    }
}

function local_complementation(node) {
    var keys = Object.keys(ngbh[node]);
    for (var i=0; i < keys.length; ++i) {
        for (var j=i+1; j < keys.length; ++j) {
            toggle_edge(keys[i], keys[j]);
        }
        vops[i] = times_table[vops[keys[i]]][sqz_h];
    }
    vops[node] = times_table[vops[node]][msqx_h];
}

function act_local_rotation(node, operation) {
    var rotation = clifford[operation];
    vops[node] = times_table[rotation][vops[node]];
}

function act_hadamard(node){
    act_local_rotation(node, 10);
}

function is_sole_member(node, group){
    return group.length == 1 && group[0] == node;
}

function act_cz(a, b){
    if (is_sole_member(ngbh[a], b)) {
        remove_vop(a, b);
    }
    if (is_sole_member(ngbh[b], a)) {
        remove_vop(b, a);
    }
    if (is_sole_member(ngbh[a], b)) {
        remove_vop(a, b);
    }
    var edge = has_edge(a, b);
    var new_state = cz_table[edge ? 1 : 0][vops[a]][vops[b]];
    vops[a] = new_state[1];
    vops[b] = new_state[2];
    if (new_state[0] != edge){
        toggle_edge(a, b);
    }
}


function log_graph_state() {
    console.log(vops);
    console.log(ngbh);
}

