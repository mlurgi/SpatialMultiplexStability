

from datetime import datetime

import networkx as nx
import csv
import math
from threading import Lock
from copy import copy, deepcopy

#import matplotlib
#matplotlib.use('gtk')

from pylab import ion, show, figure, draw

from web import Network
from network_creator import obtain_interactions_network
from ecosystem import Ecosystem

from utilities import get_out_row, get_eco_state_row, plot_populations_series, calculate_stability_measures, ThreadNetStats, ThreadEcosystemStats, write_spatial_analysis

from configure import ITERATIONS, HABITAT_LOSS, HABITAT_LOSS_ITER, HABITAT_RECOVERY, HABITAT_RECOVERY_ITER 
from configure import INVASION, INVASION_ITER, NETWORK_RESET, SPATIAL_VARIATION
from configure import REFRESH_RATE, REMOVAL_LEVEL, REMOVAL_FRACTION, EXTINCTION_EVENT, TIME_WINDOW
from configure import SRC_NET_FILE, READ_FILE_NETWORK, NETWORK_RECORD, ITERATIONS_TO_RECORD, INT_STRENGTHS, RECORD_SPATIAL_VAR


if __name__ == '__main__':
    
    start_sim = datetime.now()
    
    header_names = ['iteration','S', 'L', 'L/S','C', 'T', 'B', 'I', 'Ca', 'Loop', 'NCycles', 'O', 'T-B', 'T-I', 'I-I', 'I-B', 'GenSD', 'VulSD', 'MxSim', 'MaxChainLength', 'MeanFoodChainLength', 'ChnSD', 'ChnNo', 'complexity', 'dynamic_complexity', 'components', 'cc', 'compartmentalisation', 'mean_tp', 'sd_tp', 'stable', 'mean_cv', 'nodf', 'h2', 'G_qi', 'V_qi', 'G_q', 'V_q', 'spatially_stable', 'mean_cv_centroid', 'mean_cv_area', 'mean_cv_density'];
    file_net = open('../output/output_network.csv', 'w')
    out = csv.DictWriter(file_net, header_names)
    
    ###this is for python < 2.7
#    headers_dict = dict()
#    for n in header_names:
#        headers_dict[n] = n
#        
#    out.writerow(headers_dict)
    
    ### for python >= 2.7 comment the above block and uncomment the following line 
    out.writeheader()
    
    header_names = ['iteration', 'total_sp', 'total_count', 'prod_sp', 'prod_count', 'mut_prod_sp', 'mut_prod_count', 'herb_sp', 'herb_count', 'mut_sp', 'mut_count', 'prim_pred_sp', 'prim_pred_count', 'sec_pred_sp', 'sec_pred_count', 'shannon_index', 'shannon_eq', 'shannon_index_prods', 'shannon_eq_prods', 'shannon_index_herbs', 'shannon_eq_herbs', 'shannon_index_interm', 'shannon_eq_interm', 'shannon_index_top', 'shannon_eq_top']
    file_eco = open('../output/output_ecosystem.csv', 'w')
    out_eco = csv.DictWriter(file_eco, header_names)
    
    ###this is for python < 2.7
#    headers_dict = dict()
#    for n in header_names:
#        headers_dict[n] = n
#        
#    out_eco.writerow(headers_dict)
    
    ### for python >= 2.7 comment the above block and uncomment the following line
    out_eco.writeheader()
    
    network_file = '../output/'+SRC_NET_FILE
    if READ_FILE_NETWORK:
        graph = nx.read_graphml(network_file)
        net = Network(graph)
        
        print 'connectance = ', net.connectance()
        
        tls = net.get_trophic_levels()
        
        top, top_preds = net.top_predators()
        basal, basal_sps = net.basal()
        for u,v in net.edges():
            if u in basal_sps and v in top_preds and tls[v] == 3:
                net.remove_edge(u,v)
                
        print 'new connectance = ', net.connectance()
        
#        layout = nx.circular_layout(net)
#            
#        fig = figure()
#        network_plot = fig.add_subplot(111)
#        nx.draw_networkx(net, layout, ax=network_plot)
#    
#        print 'S original =', net.order(), 'L original =', net.size(), 'C original =', net.connectance()
#        show()
#        print tls
        
    else:
        net = obtain_interactions_network()
        net_to_save = net.copy()
        nx.write_graphml(net_to_save, network_file)
    
    ecosystem = Ecosystem(net, drawing=True)
    ecosystem.initialise_world(True)  
    ecosystem.draw_species_distribution()
    
    out_row = get_out_row(0, net, '', 0, '','')
    out.writerow(out_row)
    
#    iteration_to_reset = (int) (math.ceil(ITERATIONS*NETWORK_RESET))
    
    out_row_eco = get_eco_state_row(0, ecosystem)
    out_eco.writerow(out_row_eco)
    
#    print ecosystem.get_groups_counts()   
#    plot_series = []
#    plot_prods = []
#    plot_mut_prods = []
#    plot_herbs = []
#    plot_muts = []
#    plot_prim = []
#    plot_sec = []
#    
#    plot_prods_rep = []
#    plot_mut_prods_rep = []
#    plot_herbs_rep = []
#    plot_muts_rep = []
#    plot_prim_rep = []
#    plot_sec_rep = []
#    
#    plot_prods_inmig = []
#    plot_mut_prods_inmig = []
#    plot_herbs_inmig = []
#    plot_muts_inmig = []
#    plot_prim_inmig = []
#    plot_sec_inmig = []
#    
#    plot_prods_dead = []
#    plot_mut_prods_dead = []
#    plot_herbs_dead = []
#    plot_muts_dead = []
#    plot_prim_dead = []
#    plot_sec_dead = []
#    
#    fig = figure(figsize=(27,12))
#    plot = fig.add_subplot(212)
#    plot_rep = fig.add_subplot(231)
#    plot_inmig = fig.add_subplot(232)
#    plot_dead = fig.add_subplot(233)
#    
#    populations_historical_before = dict()
#    populations_historical_after = dict()
    
    network_stats_lock = Lock()
    ecosystem_stats_lock = Lock()
    threads = []
    
    series_counts = dict()
    
    if SPATIAL_VARIATION:
        centroids_counts = dict()
        areas_counts = dict()
    
    ##this structure holds the numbers of immigration, birth and dead of individuals
    ##for each species during the last ITERATIONS_TO_RECORD iterations
    cumulative_sps_stats = dict.fromkeys(net.nodes(), None)
    stats = ['immigrants', 'born', 'dead', 'tps']
    for sp in cumulative_sps_stats.keys():
        cumulative_sps_stats[sp] = dict.fromkeys(stats, 0)
    
    threshold_iter = math.ceil(ITERATIONS - (ITERATIONS*ITERATIONS_TO_RECORD))
    
    for i in range(1, ITERATIONS+1):
        print i
        
        ecosystem.count_individuals()
        ecosystem.update_world()
        ecosystem.draw_species_distribution()
        
        if i >= threshold_iter:
            for sp in cumulative_sps_stats.keys():
                sp_stats = cumulative_sps_stats[sp]
                
                sp_stats['immigrants'] += ecosystem.new_inds_inmigration[sp]
                sp_stats['born'] += ecosystem.new_inds_reproduction[sp]
                sp_stats['dead'] += ecosystem.dead_individuals[sp] 
                    
                    
#        if i%REFRESH_RATE == 0 and i>3:
#            ecosystem.draw_species_distribution()
#            gc = ecosystem.get_groups_counts()
#            if i == EXTINCTION_EVENT:
#                removed = ecosystem.extinguish_species(REMOVAL_LEVEL, REMOVAL_FRACTION)
#            
#            if i >= (EXTINCTION_EVENT - TIME_WINDOW) and i <= EXTINCTION_EVENT:
#                populations_historical_before[i] = ecosystem.populations
#            
#            if i > EXTINCTION_EVENT and i <= (EXTINCTION_EVENT + TIME_WINDOW):
#                populations_historical_after[i] = ecosystem.populations
#            
#            if i == (EXTINCTION_EVENT + TIME_WINDOW):
#                calculate_stability_measures(populations_historical_before, populations_historical_after, ecosystem.species_scl, mutualistic_producers)
#            
#            plot_series.append(i)
#            a,b = gc['prods']
#            plot_prods.append(b)
#            
#            a,b = gc['prods_new']
#            plot_prods_rep.append(a)
#            plot_prods_inmig.append(b)
#            
#            a = gc['prods_dead']
#            plot_prods_dead.append(a)
#            
#            a,b = gc['mut_prods']
#            plot_mut_prods.append(b)
#            
#            a,b = gc['mut_prods_new']
#            plot_mut_prods_rep.append(a)
#            plot_mut_prods_inmig.append(b)
#            
#            a = gc['mut_prods_dead']
#            plot_mut_prods_dead.append(a)
#            
#            a,b = gc['herbs']
#            plot_herbs.append(b)
#            
#            a,b = gc['herbs_new']
#            plot_herbs_rep.append(a)
#            plot_herbs_inmig.append(b)
#            
#            a = gc['herbs_dead']
#            plot_herbs_dead.append(a)
#            
#            a,b = gc['muts']
#            plot_muts.append(b)
#            
#            a,b = gc['muts_new']
#            plot_muts_rep.append(a)
#            plot_muts_inmig.append(b)
#            
#            a = gc['muts_dead']
#            plot_muts_dead.append(a)
#            
#            a,b = gc['prim_preds']
#            plot_prim.append(b)
#            
#            a,b = gc['prim_preds_new']
#            plot_prim_rep.append(a)
#            plot_prim_inmig.append(b)
#            
#            a = gc['prim_preds_dead']
#            plot_prim_dead.append(a)
#            
#            a,b = gc['second_preds']
#            plot_sec.append(b)
#            
#            a,b = gc['second_preds_new']
#            plot_sec_rep.append(a)
#            plot_sec_inmig.append(b)
#            
#            a = gc['second_preds_dead']
#            plot_sec_dead.append(a)
#            
#            plot_populations_series(plot, plot_series, plot_prods, plot_mut_prods, plot_herbs, plot_muts, plot_prim, plot_sec, title='populations')
##            draw()
#            plot_populations_series(plot_rep, plot_series, plot_prods_rep, plot_mut_prods_rep, plot_herbs_rep, plot_muts_rep, plot_prim_rep, plot_sec_rep, title='reproduction')
##            draw()
#            plot_populations_series(plot_inmig, plot_series, plot_prods_inmig, plot_mut_prods_inmig, plot_herbs_inmig, plot_muts_inmig, plot_prim_inmig, plot_sec_inmig, title='inmigration')
#            
#            plot_populations_series(plot_dead, plot_series, plot_prods_dead, plot_mut_prods_dead, plot_herbs_dead, plot_muts_dead, plot_prim_dead, plot_sec_dead, title='death')
#            
#            draw()
            
        if HABITAT_LOSS and i == HABITAT_LOSS_ITER:
            net_temp = ecosystem.realised_net.copy()
#            layout_temp = nx.circular_layout(net_temp)
#            
#            fig_temp = figure()
#            network_p_temp = fig_temp.add_subplot(111)
#            nx.draw_networkx(net_temp, layout_temp, ax=network_p_temp)
#    
#            print 'S realised =', net_temp.order(), 'L realised =', net_temp.size(), 'C realised =', net_temp.connectance()
#            
            ecosystem.clear_realised_network()
            
            #out_row = get_out_row(i, net_temp)
            #out.writerow(out_row)
            
            ecosystem.apply_habitat_loss()
            
            #ecosystem.draw_species_distribution()
#        
#        if INVASION and i == INVASION_ITER:
#            net_temp = ecosystem.realised_net.copy()
#            ecosystem.invade(invaders)
#            
#            out_row = get_out_row(i, net_temp)
#            out.writerow(out_row)
#    
#        if i == (ITERATIONS - iteration_to_reset):
#            ecosystem.clear_realised_network()
        
        
        if HABITAT_RECOVERY and i == HABITAT_RECOVERY_ITER:
            net_temp = ecosystem.realised_net.copy()
            ecosystem.clear_realised_network()
            ecosystem.recover_habitat()
          
        eco_temp = copy(ecosystem)
        if SPATIAL_VARIATION and i%20 == 0:
            eco_thread = ThreadEcosystemStats(ecosystem_stats_lock, out_eco, eco_temp, i, series_counts, centroids_counts, areas_counts)
        else:
            eco_thread = ThreadEcosystemStats(ecosystem_stats_lock, out_eco, eco_temp, i, series_counts)
                                       
        threads.append(eco_thread)
        eco_thread.start()
    
        #calculate network metrics
        if i%NETWORK_RECORD == 0 or i == ITERATIONS:
            net_temp = ecosystem.realised_net.copy()
            
            ##here we obtain the trophic position of each species so at the end we can calculate
            ##its mean and standard deviation for the species statistics
            tps, a, b = net_temp.find_trophic_positions()
            for sp in cumulative_sps_stats.keys():
                if cumulative_sps_stats[sp]['tps'] == 0:
                    cumulative_sps_stats[sp]['tps'] = []
                
                if tps.has_key(sp):
                    cumulative_sps_stats[sp]['tps'].append(tps[sp])
            
            if SPATIAL_VARIATION:
                thread = ThreadNetStats(network_stats_lock, out, net_temp, i, NETWORK_RECORD, series_counts, eco_thread, INT_STRENGTHS, centroids_counts, areas_counts)
            else:
                thread = ThreadNetStats(network_stats_lock, out, net_temp, i, NETWORK_RECORD, series_counts, eco_thread, INT_STRENGTHS)
            
            threads.append(thread)
            thread.start()
            ecosystem.clear_realised_network()
    

        ##calculate spatial variation metrics
        if SPATIAL_VARIATION and (i%RECORD_SPATIAL_VAR == 0 or i == ITERATIONS):
            start = datetime.now()
            write_spatial_analysis(ecosystem, i)
            stop = datetime.now()
            elapsed = stop-start
            print elapsed

    for t in threads:
        t.join()

    file_net.close()
    file_eco.close()
    
    
    # here we write the output file for the species populations dynamics
    header_names = ['iteration']
    for sp in sorted(ecosystem.species):
        header_names.append(sp)
        
    file_populations = open('../output/output_populations.csv', 'w')
    out_populations = csv.DictWriter(file_populations, header_names)
    
    out_populations.writeheader()
    
    out_row_pops = dict()
    for iter in series_counts.keys():
        out_row_pops['iteration'] = iter
        for sp in sorted(series_counts[iter].keys()):
            out_row_pops[sp] = series_counts[iter][sp]
        
        out_populations.writerow(out_row_pops)
        
    file_populations.close()
    
    if SPATIAL_VARIATION:
        file_centroids = open('../output/output_centroids.csv', 'w')
        out_centroids = csv.DictWriter(file_centroids, header_names)
        
        out_centroids.writeheader()
        
        out_row_cents = dict()
        for iter in centroids_counts.keys():
            out_row_cents['iteration'] = iter
            for sp in sorted(centroids_counts[iter].keys()):
                out_row_cents[sp] = centroids_counts[iter][sp]
            
            out_centroids.writerow(out_row_cents)
            
        file_centroids.close()
        
        file_areas = open('../output/output_areas.csv', 'w')
        out_areas = csv.DictWriter(file_areas, header_names)
        
        out_areas.writeheader()
        
        out_row_areas = dict()
        for iter in areas_counts.keys():
            out_row_areas['iteration'] = iter
            for sp in sorted(areas_counts[iter].keys()):
                out_row_areas[sp] = areas_counts[iter][sp]
            
            out_areas.writerow(out_row_areas)
            
        file_areas.close()
    
    
    header_names = ['species', 'init_tl', 'final_tl', 'mutualist', 'mutualistic_producer', 'mean_tp', 'tp_sd', 'individuals', 'immigrants', 'born', 'dead']
    file_species = open('../output/output_species.csv', 'w')
    out_species = csv.DictWriter(file_species, header_names)
    
    out_species.writeheader()
    out_row_species = dict()
    
    for sp in sorted(cumulative_sps_stats.keys()):
        out_row_species['species'] = sp
        
        init_tls = net.get_trophic_levels()
        out_row_species['init_tl'] = init_tls[sp]
        
        final_tls = net_temp.get_trophic_levels()
        if final_tls.has_key(sp):
            out_row_species['final_tl'] = final_tls[sp]
        else:
            out_row_species['final_tl'] = 'N/A'
        
        out_row_species['mutualist'] = net.node[sp]['mut']
        out_row_species['mutualistic_producer'] = net.node[sp]['mut_prod']
        
        tps = cumulative_sps_stats[sp]['tps']
        if len(tps) == 0:
            mean_tps = 'N/A'
            sd_tps = 'N/A'
        else:
            mean_tps = sum(tps)/len(tps)
            sd_tps = 0.0
            for n in tps:
                sd_tps += (n-mean_tps)**2
        
            sd_tps = math.sqrt(sd_tps/len(tps))
        
        out_row_species['mean_tp'] = mean_tps
        out_row_species['tp_sd'] = sd_tps
        
        out_row_species['individuals'] = series_counts[ITERATIONS][sp]
        out_row_species['immigrants'] = cumulative_sps_stats[sp]['immigrants']
        out_row_species['born'] = cumulative_sps_stats[sp]['born']
        out_row_species['dead'] = cumulative_sps_stats[sp]['dead']
        
        out_species.writerow(out_row_species)
        
    file_species.close()
    
    stop_sim = datetime.now()
    elapsed_sim = stop_sim-start_sim
    print 'time for simulation' , elapsed_sim
    
    
    #ecosystem.draw_species_distribution()
    
    #layout = nx.graphviz_layout(net, prog='dot', args='-Gnodesep=.07, -Granksep=.1, -Grankdir=BT')
    layout = nx.circular_layout(net)
            
    fig = figure()
    network_plot = fig.add_subplot(111)
    nx.draw_networkx(net, layout, ax=network_plot)
    
    print 'S original =', net.order(), 'L original =', net.size(), 'C original =', net.connectance()
#    
#    net_final = ecosystem.realised_net.copy()
#    layout2 = nx.circular_layout(net_final)
#            
#    fig2 = figure()
#    network_plot2 = fig2.add_subplot(111)
#    nx.draw_networkx(net_final, layout2, ax=network_plot2)
#    
#    print 'S realised =', net_final.order(), 'L realised =', net_final.size(), 'C realised =', net_final.connectance()

    show()
    
    
    