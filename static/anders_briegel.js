var abj = {};
abj.ngbh = {};
abj.vops = {};
abj.meta = {};
ngbh = abj.ngbh;
vops = abj.vops;
meta = abj.meta;
abj.add_node = function(node, m) {
    ngbh[node] = {};
    vops[node] = clifford.hadamard;
    meta[node] = m ? m : {};
};

abj.add_nodes = function(nodes) {
    nodes.forEach(add_node);
};

abj.add_edge = function(a, b) {
    ngbh[a][b] = true;
    ngbh[b][a] = true;
};

abj.add_edges = function(edges) {
    edges.forEach(function(e) {
        add_edge(e[0], e[1]);
    });
};

abj.del_edge = function(a, b) {
    delete ngbh[a][b];
    delete ngbh[b][a];
};

abj.has_edge = function(a, b) {
    return Object.prototype.hasOwnProperty.call(ngbh[a], b);
};

abj.toggle_edge = function(a, b) {
    if (has_edge(a, b)) {
        del_edge(a, b);
    } else {
        add_edge(a, b);
    }
};

abj.get_swap = function(node, avoid) {
    for (var i in ngbh[node]) {
        if (i != avoid) {return i;}
    }
    return avoid;
};

abj.remove_vop = function(node, avoid) {
    var swap_qubit = get_swap(node, avoid);
    var decomposition = decompositions[vops[node]];
    for (var i=decomposition.length-1; i >=0; --i) {
        var v = decomposition[i];
        local_complementation(v == "x" ? a : swap_qubit);
    }
};

abj.local_complementation = function(node) {
    var keys = Object.keys(ngbh[node]);
    for (var i=0; i < keys.length; ++i) {
        for (var j=i+1; j < keys.length; ++j) {
            toggle_edge(keys[i], keys[j]);
        }
        vops[i] = times_table[vops[keys[i]]][sqz_h];
    }
    vops[node] = times_table[vops[node]][msqx_h];
};

abj.act_local_rotation = function(node, operation) {
    var rotation = clifford[operation];
    vops[node] = times_table[rotation][vops[node]];
};

abj.act_hadamard = function(node){
    act_local_rotation(node, 10);
};

abj.is_sole_member = function(node, group){
    return group.length == 1 && group[0] == node;
};

abj.act_cz = function(a, b){
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
};

abj.edgelist = function() {
    var seen = {};
    var output = [];
    for (var i in ngbh) {
        for (var j in ngbh[i]) {
            if (!Object.prototype.hasOwnProperty.call(seen, j)){
                output.push([i, j]);
            }
        }
        seen[i] = true;
    }
    return output;
};

abj.log_graph_state = function() {
    console.log(JSON.stringify(vops));
    console.log(JSON.stringify(ngbh));
};

