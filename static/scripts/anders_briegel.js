var abj = {};
abj.node = {};
abj.adj = {};

abj.add_node = function(node, meta) {
    abj.adj[node] = {};
    abj.node[node] = {};
    abj.node[node].vop = tables.clifford.hadamard;
    Object.assign(abj.node[node], meta);
};

abj.add_nodes = function(nodes) {
    nodes.forEach(add_node);
};

abj.del_node = function(node) {
    for (var i in abj.adj[node]) {
        abj.del_edge(node, i);
    }
    delete abj.node[node];
};

abj.add_edge = function(a, b) {
    abj.adj[a][b] = {};
    abj.adj[b][a] = {};
};

abj.add_edges = function(edges) {
    edges.forEach(function(e) {
        add_edge(e[0], e[1]);
    });
};

abj.del_edge = function(a, b) {
    delete abj.adj[a][b];
    delete abj.adj[b][a];
};

abj.has_edge = function(a, b) {
    return Object.prototype.hasOwnProperty.call(abj.adj[a], b);
};

abj.toggle_edge = function(a, b) {
    if (abj.has_edge(a, b)) {
        abj.del_edge(a, b);
    } else {
        abj.add_edge(a, b);
    }
};

abj.get_swap = function(node, avoid) {
    for (var i in abj.adj[node]) {
        if (i != avoid) {
            return i;
        }
    }
    return avoid;
};

abj.remove_vop = function(node, avoid) {
    var swap_qubit = get_swap(node, avoid);
    var decomposition = decompositions[abj.node[node].vop];
    for (var i = decomposition.length - 1; i >= 0; --i) {
        var v = decomposition[i];
        local_complementation(v == "x" ? a : swap_qubit);
    }
};

abj.local_complementation = function(node) {
    var keys = Object.keys(abj.adj[node]);
    for (var i = 0; i < keys.length; ++i) {
        for (var j = i + 1; j < keys.length; ++j) {
            abj.toggle_edge(keys[i], keys[j]);
        }
        abj.node[i].vop = tables.times_table[abj.node[keys[i]].vop][6];
    }
    abj.node[node].vop = tables.times_table[abj.node[node].vop][14];
};

abj.act_local_rotation = function(node, operation) {
    var rotation = tables.clifford[operation];
    abj.node[node].vop = tables.times_table[rotation][abj.node[node].vop];
};

abj.act_hadamard = function(node) {
    abj.act_local_rotation(node, 10);
};

abj.is_sole_member = function(node, group) {
    return group.length == 1 && group[0] == node;
};

abj.act_cz = function(a, b) {
    if (abj.is_sole_member(abj.adj[a], b)) {
        remove_vop(a, b);
    }
    if (abj.is_sole_member(abj.adj[b], a)) {
        remove_vop(b, a);
    }
    if (abj.is_sole_member(abj.adj[a], b)) {
        remove_vop(a, b);
    }
    var edge = abj.has_edge(a, b);
    var new_state = tables.cz_table[edge ? 1 : 0][abj.node[a].vop][abj.node[b].vop];
    abj.node[a].vop = new_state[1];
    abj.node[b].vop = new_state[2];
    if (new_state[0] != edge) {
        abj.toggle_edge(a, b);
    }
};

abj.edgelist = function() {
    var seen = {};
    var output = [];
    for (var i in abj.adj) {
        for (var j in abj.adj[i]) {
            if (!Object.prototype.hasOwnProperty.call(seen, j)) {
                output.push([i, j]);
            }
        }
        seen[i] = true;
    }
    return output;
};

abj.log_graph_state = function() {
    console.log(JSON.stringify(abj.node));
    console.log(JSON.stringify(abj.adj));
};

abj.update = function(newState) {
    abj.node = newState.node;
    abj.adj = newState.adj;
};

abj.order = function(){
    return Object.keys(abj.node).length;
};

