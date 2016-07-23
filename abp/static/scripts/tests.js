QUnit.test( "Adding nodes", function( assert ) {
    abj.add_node(0);
    assert.ok(abj.node[0].vop === 10, JSON.stringify(abj.node));
});
