from abp import make_tables
import cProfile, pstats, StringIO

unitaries = make_tables.get_unitaries()

profiler = cProfile.Profile()
profiler.enable()
make_tables.get_cz_table(unitaries)
profiler.disable()

# Print output
stats = pstats.Stats(profiler).strip_dirs().sort_stats('tottime')
stats.print_stats(10)
