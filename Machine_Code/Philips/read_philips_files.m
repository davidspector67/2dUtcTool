function[x_dim, y_dim] = read_philips_files(filepath)

    if filepath(length(filepath)-3:length(filepath)) == '.mat'
        load(filepath);
        exist rf_data_all_fund;
        if ans == 1;
            dims = size(rf_data_all_fund{1,1}{1,1});
            y_dim = dims(1);
            x_dim = dims(2);
        else
            x_dim = -1;
            y_dim = -1;
        end
    else
        x_dim = -1;
        y_dim = -1;
    end
end
